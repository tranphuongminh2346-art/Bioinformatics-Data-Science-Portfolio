"""
Portfolio Master Test Runner
Author: Portfolio Creator
Description: Programmatically executes all unit test suites across all daily projects.
             Prints pretty status summaries and logs execution durations.
             Smart cache mode: skips tests that already PASSED in a previous run.
             Pass --full to force re-run every test regardless of cache.
Language: English (100%)
"""

import os
import sys
import subprocess
import time
import json

TEST_SUITES = {
    "Project 1: DNA Sequence Analyzer": "project_001_dna_sequence_analyzer/test_dna_analyzer.py",
    "Project 2: Clinical Trial Pipeline": "project_002_clinical_trial_pipeline/test_pipeline.py",
    "Project 3: Heart Disease Classifier": "project_003_heart_disease_classifier/test_model.py",
    "Project 4: Protein Coordinate Analyzer": "project_004_protein_analyzer/test_pdb_analyzer.py",
    "Project 5: Weather ETL Pipeline": "project_005_weather_etl/test_etl.py",
    "Project 6: Genomic Variant Predictor": "project_006_variant_predictor/test_variant_predictor.py",
    "Project 7: Customer Churn Predictor": "project_007_churn_predictor/test_churn.py",
    "Project 8: PubMed Citation Network": "project_008_citation_network/test_network.py",
    "Project 9: COVID-19 Trends Dashboard": "project_009_covid_dashboard/test_covid.py",
    "Project 10: RNA-Seq Expression Analyzer": "project_010_rna_seq_analyzer/test_expression.py",
    "Project 11: Job Listings Scraper": "project_011_job_scraper/test_parser.py",
    "Project 12: Medical abstracts NLP Miner": "project_012_abstracts_nlp/test_text_miner.py",
    "Project 13: Malaria Cell Classifier": "project_013_malaria_classifier/test_classifier.py",
    "Project 14: Clinical Trials REST API": "project_014_clinical_api/test_api.py",
    "Project 15: UPGMA Phylogenetic Reconstructor": "project_015_phylogenetic_tree/test_upgma.py",
    "Project 16: Housing Price Predictor": "project_016_house_predictor/test_predictor.py",
    "Project 17: Stock Price Forecaster": "project_017_stock_forecast/test_forecaster.py",
    "Project 18: Needleman-Wunsch Alignment": "project_018_sequence_alignment/test_alignment.py",
    "Project 19: Enzyme Kinetics parameter Fitter": "project_019_enzyme_kinetics/test_fitter.py",
    "Project 20: Genomic GC-Content Map Generator": "project_020_gc_content_map/test_mapper.py",
    "Project 21: Customer segmentation Clustering": "project_021_customer_segmentation/test_segmentation.py",
    "Project 22: Web Server Log Anomaly Detector": "project_022_log_anomaly_detector/test_detector.py",
    "Project 23: FASTA Header Parser & DB Loader": "project_023_fasta_db_loader/test_parser.py",
    "Project 24: Wine Quality Decision Tree": "project_024_wine_classifier/test_classifier.py",
    "Project 25: PubMed API Literature pipeline": "project_025_pubmed_api_pipeline/test_fetcher.py",
    "Project 26: Movie Collaborative Filtering": "project_026_movie_recommender/test_recommender.py",
    "Project 27: DNA Motif Gibbs Sampler Finder": "project_027_motif_finder/test_motif.py",
    "Project 28: Stock Trading Strategy Backtester": "project_028_trading_backtester/test_backtester.py",
    "Project 29: Handwritten Digits Naive Bayes": "project_029_digit_recognition/test_classifier.py",
    "Project 30: Climate Temp Anomaly Analyzer": "project_030_temperature_anomaly/test_series.py",
    "Project 31: Genotype VCF Quality Control Filter": "project_031_vcf_qc_filter/test_filter.py",
    "Project 32: PageRank Extractive Summarizer": "project_032_text_summarizer/test_summarizer.py",
    "Project 33: SVM Breast Cancer Classifier": "project_033_cancer_classifier/test_classifier.py",
    "Project 34: PCR Genomic Primer Designer": "project_034_primer_designer/test_designer.py",
    "Project 35: SQLite Index & Query Profiler": "project_035_query_profiler/test_profiler.py",
    "Project 36: DNA open Reading Frame ORF Finder": "project_036_orf_finder/test_finder.py",
    "Project 37: SMS Spam TF-IDF classifier": "project_037_sms_spam_filter/test_filter.py",
    "Project 38: Cellular Automaton Game of Life": "project_038_conway_game/test_simulator.py",
    "Project 39: Hierarchical Gene Expression Clustering": "project_039_microarray_clustering/test_clustering.py",
    "Project 40: PLINK PED/MAP Pedigree Parser": "project_040_plink_ped_parser/test_parser.py",
    "Project 41: Markov DNA Transition Sequence Simulator": "project_041_synthetic_dna_generator/test_generator.py",
    "Project 42: PCAP Packet Network Anomaly Parser": "project_042_pcap_traffic_analyzer/test_analyzer.py",
    "Project 43: Chemical Solubility Descriptor Regressor": "project_043_chem_solubility_predictor/test_predictor.py",
    "Project 44: HMM Viterbi Eukaryotic Gene Finder": "project_044_viterbi_gene_finder/test_finder.py",
    "Project 45: ECG Heart Rate Variability Extractor": "project_045_heart_rate_variability/test_hrv.py",
    "Project 46: Redis-like LRU persistent AOF database": "project_046_redis_cache_simulator/test_simulator.py",
    "Project 47: Acid-Base pH Titration Curve Simulator": "project_047_ph_titration_curve/test_titration.py",
    "Project 48: Burrows-Wheeler Transform DNA Indexer": "project_048_dna_kmer_index/test_indexer.py",
    "Project 49: NMF Document Topic Modeler": "project_049_news_topic_modeling/test_modeler.py",
    "Project 50: Hospital Patient Admission Forecaster": "project_050_patient_admission_forecaster/test_forecaster.py",
    "Project 51: PHYLIP Sequence Alignment Parser": "project_051_phylip_alignment_parser/test_parser.py",
    "Project 52: Mass Spectrometry MS Signal Peak Finder": "project_052_mass_spec_peak_finder/test_peaks.py",
    "Project 53: Satellite NDVI Matrix Calculator": "project_053_satellite_ndvi_calculator/test_ndvi.py",
    "Project 54: GWAS Manhattan & Q-Q Plotter": "project_054_gwas_manhattan_plot/test_plotter.py",
    "Project 55: Cell Migration Particle Tracker": "project_055_cell_migration_tracker/test_tracker.py",
    "Project 56: EEG Brainwave Band Power FFT Extractor": "project_056_eeg_band_power/test_eeg.py",
    "Project 57: Triangular Exchange Arbitrage Detector": "project_057_cryptocurrency_arbitrage/test_arbitrage.py",
    "Project 58: Backtracking DNA Restriction Mapper": "project_058_restriction_map/test_mapper.py",
    "Project 59: Verlet Lennard-Jones Dynamics Simulator": "project_059_molecular_dynamics_lj/test_dynamics.py",
    "Project 60: Autoencoder Log Reconstruction Anomaly": "project_060_log_anomaly_autoencoder/test_autoencoder.py",
    "Project 61: FASTQ Phred Quality QC Parser": "project_061_fastq_quality_qc/test_qc.py",
    "Project 62: Fisher GO Term Enrichment Hypergeometric": "project_062_gene_ontology_enrichment/test_enrichment.py",
    "Project 63: Regex Clinical Concept Medical NER": "project_063_clinical_concept_ner/test_ner.py",
    "Project 64: Chou-Fasman Protein Sec Structure Predictor": "project_064_protein_sec_structure/test_predictor.py",
    "Project 65: TCP Segment Sequence Reassembler": "project_065_tcp_flow_reassembler/test_reassembler.py",
    "Project 66: PCA scRNA-seq Cell Clusterer": "project_066_single_cell_tsne/test_clusterer.py",
    "Project 67: Nussinov RNA Fold Dynamic Programming": "project_067_rna_secondary_structure/test_folder.py",
    "Project 68: Microbiome Shannon Ecological Diversity": "project_068_microbiome_diversity/test_diversity.py",
    "Project 69: Multi-sample VCF Stats & Ti/Tv Ratio": "project_069_variant_call_format_stats/test_stats.py",
    "Project 70: PDB 3D Contact Map & Distance Matrix": "project_070_pdb_contact_map/test_contact.py",
    "Project 71: MSA Consensus Sequence & PSSM Builder": "project_071_msa_consensus_builder/test_consensus.py",
    "Project 72: Differential Expression Volcano Plot Generator": "project_072_expression_volcano_plot/test_plotter.py",
    "Project 73: CRISPR-Cas9 sgRNA Target & Off-target Finder": "project_073_crispr_ggrna_designer/test_designer.py",
    "Project 74: K-mer Counting with Bloom Filters": "project_074_dna_kmer_counter_bloom/test_bloom.py",
    "Project 75: Metagenomic Taxonomic Profiler": "project_075_metagenomic_taxonomic_profiler/test_profiler.py",
    "Project 76: EM Haplotype Phasing": "project_076_haplotype_phasing_em/test_phaser.py",
    "Project 77: Peptide Isoelectric Point & Net Charge Calculator": "project_077_protein_isoelectric_point/test_calc.py",
    "Project 78: GFF3 Genomic Feature Annotation Parser": "project_078_gff3_annotation_parser/test_parser.py",
    "Project 79: RNA-seq Splice Junction Donor/Acceptor Mapper": "project_079_splicing_junction_finder/test_finder.py",
    "Project 80: Phylogenetic Non-parametric Bootstrap Resampler": "project_080_phylogenetic_bootstrap/test_bootstrap.py",
    "Project 81: Tabular Isolation Forest Anomaly Detector": "project_081_isolation_forest_anomaly/test_anomaly.py",
    "Project 82: Decision Tree Gradient Boosting Regressor": "project_082_gradient_boosting_regressor/test_boosting.py",
    "Project 83: Rule-based VADER Text Sentiment Analyzer": "project_083_text_sentiment_vader/test_sentiment.py",
    "Project 84: TF-IDF Content-Based Recommendation Engine": "project_084_content_based_recommender/test_recommender.py",
    "Project 85: Linear Discriminant Analysis Classifier": "project_085_linear_discriminant_analysis/test_lda.py",
    "Project 86: Automated K-Means Elbow & Silhouette Clusterer": "project_086_kmeans_elbow_silhouette/test_optimizer.py",
    "Project 87: Continuous Gaussian Naive Bayes Classifier": "project_087_naive_bayes_gaussian/test_nb.py",
    "Project 88: Skip-Gram Word2Vec Embeddings Trainer": "project_088_word2vec_skipgram_embeddings/test_word2vec.py",
    "Project 89: Lightweight Backpropagation MLP Classifier": "project_089_lightweight_mlp_classifier/test_mlp.py",
    "Project 90: Agglomerative Hierarchical Clusterer": "project_090_hierarchical_agglomerative_clustering/test_agglomerative.py",
    "Project 91: MDP Value Iteration Grid World Solver": "project_091_markov_decision_process_grid/test_mdp.py",
    "Project 92: Principal Component Regression Pipeline": "project_092_principal_component_regression/test_pcr.py",
    "Project 93: Real-Time Event Stream Sliding Window Aggregator": "project_093_sliding_window_aggregator/test_aggregator.py",
    "Project 94: Columnar Parquet File Decoder": "project_094_parquet_file_reader/test_reader.py",
    "Project 95: High-Concurrency Token Bucket Rate Limiter": "project_095_token_bucket_rate_limiter/test_limiter.py",
    "Project 96: In-Memory Pub/Sub Message Broker": "project_096_pubsub_message_broker/test_pubsub.py",
    "Project 97: JSON Schema Validator Engine": "project_097_json_schema_validator/test_validator.py",
    "Project 98: Out-of-Core Large CSV Stream Chunk Processor": "project_098_csv_stream_chunk_processor/test_processor.py",
    "Project 99: Data Lineage DAG Tracker": "project_099_data_lineage_tracker/test_tracker.py",
    "Project 100: SQL Database Migration Runner & Version Control": "project_100_database_migration_engine/test_migration.py",
    "Project 101: Distributed Consistent Hashing Ring": "project_101_consistent_hashing_ring/test_hashing.py",
    "Project 102: Structured Web Server Log Regex ETL": "project_102_log_stream_parser_regex/test_parser.py",
    "Project 103: 2D Sobel Spatial Edge Detector": "project_103_sobel_edge_detector/test_sobel.py",
    "Project 104: 1D Wavelet Signal Denoiser": "project_104_wavelet_signal_denoiser/test_denoiser.py",
    "Project 105: Short-Time Fourier Transform Spectrogram Generator": "project_105_audio_spectrogram_generator/test_spectrogram.py",
    "Project 106: CDF Image Histogram Equalization Engine": "project_106_image_histogram_equalization/test_equalization.py",
    "Project 107: Matrix Pattern Optical Character Recognizer": "project_107_optical_character_recognizer_grid/test_ocr.py",
    "Project 108: Frame-Difference Video Motion Detector": "project_108_motion_detection_frame_diff/test_detector.py",
    "Project 109: Gaussian and Laplacian Image Pyramids": "project_109_gaussian_laplacian_pyramid/test_pyramids.py",
    "Project 110: 1D Topological Signal Peak Prominence Detector": "project_110_peak_detector_prominence/test_peaks.py",
    "Project 111: Hybrid LRU/LFU In-Memory Caching Engine": "project_111_lru_lfu_cache_engine/test_cache.py",
    "Project 112: Dijkstra Shortest Path Graph Solver": "project_112_dijkstra_shortest_path/test_dijkstra.py",
    "Project 113: Shunting-Yard AST Expression Evaluator": "project_113_expression_evaluator_shunting_yard/test_shunting.py",
    "Project 114: Disk-Based B-Tree Index Simulator": "project_114_btree_indexing_engine/test_btree.py",
    "Project 115: Fixed-Block Memory Pool Allocator": "project_115_memory_pool_allocator/test_allocator.py",
    "Project 116: Trie Prefix Search & Autocomplete Engine": "project_116_trie_prefix_search/test_trie.py",
    "Project 117: Topological Sorting Dependency Solver": "project_117_topological_sort_dep_solver/test_topological.py",
    "Project 118: DFA Finite State Machine Regex Engine": "project_118_finite_state_machine_regex/test_fsm.py",
    "Sports Prediction Engine": "sports_prediction_engine/tests/test_engine.py",
}

# ─── Pass Cache ────────────────────────────────────────────────────────────────
# Records which tests have already PASSED so we can skip them on subsequent runs.
# Format: { "test name": "YYYY-MM-DDTHH:MM:SS" }
CACHE_FILE = "test_pass_cache.json"

def load_pass_cache() -> dict:
    """Loads the set of already-passed test names from the cache file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_pass_cache(cache: dict):
    """Persists the pass cache to disk."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def clear_pass_cache():
    """Deletes the pass cache file to force a full re-run next time."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
# ──────────────────────────────────────────────────────────────────────────────

def main():
    # ── Parse CLI flag ─────────────────────────────────────────────────────────
    full_run = "--full" in sys.argv
    reset_cache = "--reset" in sys.argv

    if reset_cache:
        clear_pass_cache()
        print("[*] Pass cache cleared. All tests will be re-run.")

    pass_cache = {} if full_run else load_pass_cache()

    # ── Reset failure log ──────────────────────────────────────────────────────
    log_path = "test_failures.log"
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("PORTFOLIO TEST RUNNER FAILURES LOG\n")
        log_file.write("=" * 70 + "\n\n")

    mode_label = "FULL RUN (cache ignored)" if full_run else "SMART RUN (skipping cached passes)"
    print("=" * 70)
    print(f"PORTFOLIO MASTER TEST RUNNER - {mode_label}")
    print("=" * 70)
    if not full_run:
        cached_count = len(pass_cache)
        print(f"[*] Tests already passed (cached): {cached_count}")
        print(f"[*] Tests to run this session    : {len(TEST_SUITES) - cached_count}")
    print("=" * 70)

    passed_count  = 0
    failed_count  = 0
    skipped_count = 0
    cached_count  = 0

    results = []

    for name, test_path in TEST_SUITES.items():

        # ── Already passed in a prior run → skip ──────────────────────────────
        if not full_run and name in pass_cache:
            print(f"[~] {name:50} : CACHED PASS ({pass_cache[name]})")
            cached_count += 1
            results.append((name, "CACHED", 0.0))
            continue

        # ── Test file / folder missing → skip ─────────────────────────────────
        if not os.path.exists(test_path):
            print(f"[-] {name:50} : SKIPPED (file not found)")
            skipped_count += 1
            results.append((name, "SKIPPED", 0.0))
            continue

        print(f"[*] Running {name}...")
        start_time = time.time()

        res = subprocess.run(
            [sys.executable, "-m", "unittest", test_path],
            capture_output=True,
            text=True
        )
        duration = time.time() - start_time

        if res.returncode == 0:
            # ── PASSED: record in cache ────────────────────────────────────────
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            pass_cache[name] = timestamp
            save_pass_cache(pass_cache)

            print(f"[+] {name:50} : PASSED ({duration:.3f}s)")
            passed_count += 1
            results.append((name, "PASSED", duration))
        else:
            # ── FAILED: remove from cache if it was there ──────────────────────
            pass_cache.pop(name, None)
            save_pass_cache(pass_cache)

            print(f"[X] {name:50} : FAILED ({duration:.3f}s)")
            print("-" * 50)
            err_output = res.stderr or res.stdout
            print(err_output)
            print("-" * 50)
            failed_count += 1
            results.append((name, "FAILED", duration))

            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"FAILURE: {name}\n")
                log_file.write(f"Path: {test_path}\n")
                log_file.write("-" * 50 + "\n")
                log_file.write(err_output + "\n")
                log_file.write("=" * 70 + "\n\n")

    # ── Summary ────────────────────────────────────────────────────────────────
    total_ok = passed_count + cached_count
    print("\n" + "=" * 70)
    print("MASTER EXECUTION RUN SUMMARY")
    print("=" * 70)
    print(f"[*] Total Projects Listed  : {len(TEST_SUITES)}")
    print(f"[+] Passed this run        : {passed_count}")
    print(f"[~] Cached passes (skipped): {cached_count}")
    print(f"[+] Total confirmed passing: {total_ok}")
    print(f"[X] Failed                 : {failed_count}")
    print(f"[-] Skipped (missing files): {skipped_count}")
    print("-" * 70)

    if failed_count > 0:
        print("[!] Execution FAILED. Some unit tests did not pass.")
        print(f"[!] Check {log_path} for details.")
        sys.exit(1)
    else:
        print("[+] Execution SUCCESSFUL. All active unit tests passed!")
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write("ALL TESTS PASSED SUCCESSFULLY!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
