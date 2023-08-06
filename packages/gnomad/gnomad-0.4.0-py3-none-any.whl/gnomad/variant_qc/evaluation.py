import logging
from collections import defaultdict
from typing import Dict, List, Optional

import hail as hl

logging.basicConfig(
    format="%(asctime)s (%(name)s %(lineno)s): %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def compute_quantile_bin(
    ht: hl.Table,
    score_expr: hl.expr.NumericExpression,
    bin_expr: Dict[str, hl.expr.BooleanExpression] = {"bin": True},
    compute_snv_indel_separately: bool = True,
    n_bins: int = 100,
    k: int = 1000,
    desc: bool = True,
) -> hl.Table:
    """
    Returns a table with a bin for each row based on quantiles of `score_expr`.

    The bin is computed by dividing the `score_expr` into `n_bins` bins containing an equal number of elements.
    This is done based on quantiles computed with hl.agg.approx_quantiles. If a single value in `score_expr` spans more
    than one bin, the rows with this value are distributed randomly across the bins it spans.

    If `compute_snv_indel_separately` is True all items in `bin_expr` will be stratified by snv / indels for the bin
    calculation. Because SNV and indel rows are mutually exclusive, they are re-combined into a single annotation. For
    example if we have the following four variants and scores and `n_bins` of 2:

    ========   =======   ======   =================   =================
    Variant    Type      Score    bin - `compute_snv_indel_separately`:
    --------   -------   ------   -------------------------------------
    \          \         \        False               True
    ========   =======   ======   =================   =================
    Var1       SNV       0.1      1                   1
    Var2       SNV       0.2      1                   2
    Var3       Indel     0.3      2                   1
    Var4       Indel     0.4      2                   2
    ========   =======   ======   =================   =================

    .. note::

        The `bin_expr` defines which data the bin(s) should be computed on. E.g., to get a biallelic quantile bin and an
        singleton quantile bin, the following could be used:

        .. code-block:: python

            bin_expr={
                'biallelic_bin': ~ht.was_split,
                'singleton_bin': ht.singleton
            }

    :param ht: Input Table
    :param score_expr: Expression containing the score
    :param bin_expr: Quantile bin(s) to be computed (see notes)
    :param compute_snv_indel_separately: Should all `bin_expr` items be stratified by snv / indels
    :param n_bins: Number of bins to bin the data into
    :param k: The `k` parameter of approx_quantiles
    :param desc: Whether to bin the score in descending order
    :return: Table with the quantile bins
    """
    import math

    def quantiles_to_bin_boundaries(quantiles: List[int]) -> Dict:
        """
        Merges bins with the same boundaries into a unique bin while keeping track of
        which bins have been merged and the global index of all bins.

        :param quantiles: Original bins boundaries
        :return: (dict of the indices of bins for which multiple bins were collapsed -> number of bins collapsed,
                  Global indices of merged bins,
                  Merged bins boundaries)
        """

        # Pad the quantiles to create boundaries for the first and last bins
        bin_boundaries = [-math.inf] + quantiles + [math.inf]
        merged_bins = defaultdict(int)

        # If every quantile has a unique value, then bin boudaries are unique
        # and can be passed to binary_search as-is
        if len(quantiles) == len(set(quantiles)):
            return dict(
                merged_bins=merged_bins,
                global_bin_indices=list(range(len(bin_boundaries))),
                bin_boundaries=bin_boundaries,
            )

        indexed_bins = list(enumerate(bin_boundaries))
        i = 1
        while i < len(indexed_bins):
            if indexed_bins[i - 1][1] == indexed_bins[i][1]:
                merged_bins[i - 1] += 1
                indexed_bins.pop(i)
            else:
                i += 1

        return dict(
            merged_bins=merged_bins,
            global_bin_indices=[x[0] for x in indexed_bins],
            bin_boundaries=[x[1] for x in indexed_bins],
        )

    if compute_snv_indel_separately:
        # For each bin, add a SNV / indel stratification
        bin_expr = {
            f"{bin_id}_{snv}": (bin_expr & snv_expr)
            for bin_id, bin_expr in bin_expr.items()
            for snv, snv_expr in [("snv", ht.snv), ("indel", ~ht.snv)]
        }

    bin_ht = ht.annotate(
        **{f"_filter_{bin_id}": bin_expr for bin_id, bin_expr in bin_expr.items()},
        _score=score_expr,
    )

    logger.info(
        f"Adding quantile bins using approximate_quantiles binned into {n_bins}, using k={k}"
    )
    bin_stats = bin_ht.aggregate(
        hl.struct(
            **{
                bin_id: hl.agg.filter(
                    bin_ht[f"_filter_{bin_id}"],
                    hl.struct(
                        n=hl.agg.count(),
                        quantiles=hl.agg.approx_quantiles(
                            bin_ht._score, [x / (n_bins) for x in range(1, n_bins)], k=k
                        ),
                    ),
                )
                for bin_id in bin_expr
            }
        )
    )

    # Take care of bins with duplicated boundaries
    bin_stats = bin_stats.annotate(
        **{
            rname: bin_stats[rname].annotate(
                **quantiles_to_bin_boundaries(bin_stats[rname].quantiles)
            )
            for rname in bin_stats
        }
    )

    bin_ht = bin_ht.annotate_globals(
        bin_stats=hl.literal(
            bin_stats,
            dtype=hl.tstruct(
                **{
                    bin_id: hl.tstruct(
                        n=hl.tint64,
                        quantiles=hl.tarray(hl.tfloat64),
                        bin_boundaries=hl.tarray(hl.tfloat64),
                        global_bin_indices=hl.tarray(hl.tint32),
                        merged_bins=hl.tdict(hl.tint32, hl.tint32),
                    )
                    for bin_id in bin_expr
                }
            ),
        )
    )

    # Annotate the bin as the index in the unique boundaries array
    bin_ht = bin_ht.annotate(
        **{
            bin_id: hl.or_missing(
                bin_ht[f"_filter_{bin_id}"],
                hl.binary_search(
                    bin_ht.bin_stats[bin_id].bin_boundaries, bin_ht._score
                ),
            )
            for bin_id in bin_expr
        }
    )

    # Convert the bin to global bin by expanding merged bins, that is:
    # If a value falls in a bin that needs expansion, assign it randomly to one of the expanded bins
    # Otherwise, simply modify the bin to its global index (with expanded bins that is)
    bin_ht = bin_ht.select(
        **{
            bin_id: hl.cond(
                bin_ht.bin_stats[bin_id].merged_bins.contains(bin_ht[bin_id]),
                bin_ht[bin_id]
                + hl.int(
                    hl.rand_unif(
                        0, bin_ht.bin_stats[bin_id].merged_bins[bin_ht[bin_id]] + 1
                    )
                ),
                bin_ht.bin_stats[bin_id].global_bin_indices[bin_ht[bin_id]],
            )
            for bin_id in bin_expr
        }
    )

    if desc:
        bin_ht = bin_ht.annotate(
            **{bin_id: n_bins - bin_ht[bin_id] for bin_id in bin_expr}
        )

    # Because SNV and indel rows are mutually exclusive, re-combine them into a single bin.
    # Update the global bin_stats struct to reflect the change in bin names in the table
    if compute_snv_indel_separately:
        bin_expr_no_snv = {bin_id.rsplit("_", 1)[0] for bin_id in bin_ht.bin_stats}
        bin_ht = bin_ht.annotate_globals(
            bin_stats=hl.struct(
                **{
                    bin_id: hl.struct(
                        **{
                            snv: bin_ht.bin_stats[f"{bin_id}_{snv}"]
                            for snv in ["snv", "indel"]
                        }
                    )
                    for bin_id in bin_expr_no_snv
                }
            )
        )

        bin_ht = bin_ht.transmute(
            **{
                bin_id: hl.cond(
                    ht[bin_ht.key].snv,
                    bin_ht[f"{bin_id}_snv"],
                    bin_ht[f"{bin_id}_indel"],
                )
                for bin_id in bin_expr_no_snv
            }
        )

    return bin_ht


def compute_grouped_binned_ht(
    bin_ht: hl.Table, checkpoint_path: Optional[str] = None,
) -> hl.GroupedTable:
    """
    Groups a Table that has been annotated with bins based on quantiles (`compute_quantile_bin` or
    `create_binned_ht`). The table will be grouped by bin_id (bin, biallelic, etc.), contig, snv, bi_allelic and
    singleton.

    .. note::

        If performing an aggregation following this grouping (such as `score_bin_agg`) then the aggregation
        function will need to use `ht._parent` to get the origin Table from the GroupedTable for the aggregation

    :param bin_ht: Input Table with a `bin_id` annotation
    :param checkpoint_path: If provided an intermediate checkpoint table is created with all required annotations before shuffling.
    :return: Table grouped by bins(s)
    """
    # Explode the rank table by bin_id
    bin_ht = bin_ht.annotate(
        quantile_bins=hl.array(
            [
                hl.Struct(bin_id=bin_name, bin=bin_ht[bin_name])
                for bin_name in bin_ht.bin_stats
            ]
        )
    )
    bin_ht = bin_ht.explode(bin_ht.quantile_bins)
    bin_ht = bin_ht.transmute(
        bin_id=bin_ht.quantile_bins.bin_id, bin=bin_ht.quantile_bins.bin
    )
    bin_ht = bin_ht.filter(hl.is_defined(bin_ht.bin))

    if checkpoint_path is not None:
        bin_ht.checkpoint(checkpoint_path, overwrite=True)
    else:
        bin_ht = bin_ht.persist()

    # Group by bin_id, bin and additional stratification desired and compute QC metrics per bin
    return bin_ht.group_by(
        bin_id=bin_ht.bin_id,
        contig=bin_ht.locus.contig,
        snv=hl.is_snp(bin_ht.alleles[0], bin_ht.alleles[1]),
        bi_allelic=~bin_ht.was_split,
        singleton=bin_ht.singleton,
        release_adj=bin_ht.ac > 0,
        bin=bin_ht.bin,
    )._set_buffer_size(20000)


def compute_binned_truth_sample_concordance(
    ht: hl.Table, binned_score_ht: hl.Table, n_bins: int = 100
) -> hl.Table:
    """
    Determines the concordance (TP, FP, FN) between a truth sample within the callset and the samples truth data
    grouped by bins computed using `compute_quantile_bin`.

    .. note::

        The input 'ht` should contain three row fields:
            - score: value to use for quantile binning
            - GT: a CallExpression containing the genotype of the evaluation data for the sample
            - truth_GT: a CallExpression containing the genotype of the truth sample

        The input `binned_score_ht` should contain:
             - score: value used to bin the full callset
             - bin: the full callset quantile bin


    The table is grouped by global/truth sample bin and variant type and contains TP, FP and FN.

    :param ht: Input HT
    :param binned_score_ht: Table with the an annotation for quantile bin for each variant
    :param n_bins: Number of bins to bin the data into
    :return: Binned truth sample concordance HT
    """
    # Annotate score and global bin
    indexed_binned_score_ht = binned_score_ht[ht.key]
    ht = ht.annotate(
        score=indexed_binned_score_ht.score, global_bin=indexed_binned_score_ht.bin
    )

    # Annotate the truth sample quantile bin
    bin_ht = compute_quantile_bin(
        ht,
        score_expr=ht.score,
        bin_expr={"truth_sample_bin": hl.expr.bool(True)},
        n_bins=n_bins,
    )
    ht = ht.join(bin_ht, how="left")

    # Explode the global and truth sample bins
    ht = ht.annotate(
        bin=[
            hl.tuple(["global_bin", ht.global_bin]),
            hl.tuple(["truth_sample_bin", ht.truth_sample_bin]),
        ]
    )

    ht = ht.explode(ht.bin)
    ht = ht.annotate(bin_id=ht.bin[0], bin=hl.int(ht.bin[1]))

    # Compute TP, FP and FN by bin_id, variant type and bin
    return (
        ht.group_by("bin_id", "snv", "bin")
        .aggregate(
            # TP => allele is found in both data sets
            tp=hl.agg.count_where(ht.GT.is_non_ref() & ht.truth_GT.is_non_ref()),
            # FP => allele is found only in test data set
            fp=hl.agg.count_where(
                ht.GT.is_non_ref() & hl.or_else(ht.truth_GT.is_hom_ref(), True)
            ),
            # FN => allele is found in truth data only
            fn=hl.agg.count_where(
                ht.GT.is_hom_ref() & hl.or_else(ht.truth_GT.is_non_ref(), True)
            ),
            min_score=hl.agg.min(ht.score),
            max_score=hl.agg.max(ht.score),
            n_alleles=hl.agg.count(),
        )
        .repartition(5)
    )


def create_truth_sample_ht(
    mt: hl.MatrixTable, truth_mt: hl.MatrixTable, high_confidence_intervals_ht: hl.Table
) -> hl.Table:
    """
    Computes a table comparing a truth sample in callset vs the truth.

    :param mt: MT of truth sample from callset to be compared to truth
    :param truth_mt: MT of truth sample
    :param high_confidence_intervals_ht: High confidence interval HT
    :return: Table containing both the callset truth sample and the truth data
    """

    def split_filter_and_flatten_ht(
        truth_mt: hl.MatrixTable, high_confidence_intervals_ht: hl.Table
    ) -> hl.Table:
        """
        Splits a truth sample MT and filter it to the given high confidence intervals.
        Then "flatten" it as a HT by annotating GT in a row field.

        :param truth_mt: Truth sample MT
        :param high_confidence_intervals_ht: High confidence intervals
        :return: Truth sample table with GT as a row annotation
        """
        assert truth_mt.count_cols() == 1

        if not "was_split" in truth_mt.row:
            truth_mt = hl.split_multi_hts(truth_mt)

        truth_mt = truth_mt.filter_rows(
            hl.is_defined(high_confidence_intervals_ht[truth_mt.locus])
        )
        truth_mt = truth_mt.rename({"GT": "_GT"})
        return truth_mt.annotate_rows(GT=hl.agg.take(truth_mt._GT, 1)[0]).rows()

    # Load truth sample MT,
    # restrict it to high confidence intervals
    # and flatten it to a HT by annotating GT in a row annotation
    truth_ht = split_filter_and_flatten_ht(truth_mt, high_confidence_intervals_ht)
    truth_ht = truth_ht.rename({f: f"truth_{f}" for f in truth_ht.row_value})

    #  Similarly load, filter and flatten callset truth sample MT
    ht = split_filter_and_flatten_ht(mt, high_confidence_intervals_ht)

    # Outer join of truth and callset truth and annotate the score and global bin
    ht = truth_ht.join(ht, how="outer")
    ht = ht.annotate(snv=hl.is_snp(ht.alleles[0], ht.alleles[1]))

    return ht


def add_rank(
    ht: hl.Table,
    score_expr: hl.expr.NumericExpression,
    subrank_expr: Optional[Dict[str, hl.expr.BooleanExpression]] = None,
) -> hl.Table:
    """
    Adds rank based on the `score_expr`. Rank is added for snvs and indels separately.
    If one or more `subrank_expr` are provided, then subrank is added based on all sites for which the boolean expression is true.

    In addition, variant counts (snv, indel separately) is added as a global (`rank_variant_counts`).

    :param ht: input Hail Table containing variants (with QC annotations) to be ranked
    :param score_expr: the Table annotation by which ranking should be scored
    :param subrank_expr: Any subranking to be added in the form name_of_subrank: subrank_filtering_expr
    :return: Table with rankings added
    """

    key = ht.key
    if subrank_expr is None:
        subrank_expr = {}

    temp_expr = {"_score": score_expr}
    temp_expr.update({f"_{name}": expr for name, expr in subrank_expr.items()})
    rank_ht = ht.select(**temp_expr, is_snv=hl.is_snp(ht.alleles[0], ht.alleles[1]))

    rank_ht = rank_ht.key_by("_score").persist()
    scan_expr = {
        "rank": hl.cond(
            rank_ht.is_snv,
            hl.scan.count_where(rank_ht.is_snv),
            hl.scan.count_where(~rank_ht.is_snv),
        )
    }
    scan_expr.update(
        {
            name: hl.or_missing(
                rank_ht[f"_{name}"],
                hl.cond(
                    rank_ht.is_snv,
                    hl.scan.count_where(rank_ht.is_snv & rank_ht[f"_{name}"]),
                    hl.scan.count_where(~rank_ht.is_snv & rank_ht[f"_{name}"]),
                ),
            )
            for name in subrank_expr
        }
    )
    rank_ht = rank_ht.annotate(**scan_expr)

    rank_ht = rank_ht.key_by(*key).persist()
    rank_ht = rank_ht.select(*scan_expr.keys())

    ht = ht.annotate(**rank_ht[key])
    return ht
