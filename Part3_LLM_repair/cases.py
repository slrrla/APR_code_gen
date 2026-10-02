BATCHES = {
    1: ["issue_009", "issue_018_se", "issue_021_se", "issue_032_se", "issue_034",
        "issue_036", "issue_058_se", "issue_061", "issue_072", "issue_096"],
    2: ["issue_155", "issue_157", "issue_174", "issue_189", "issue_225",
        "issue_233", "issue_261", "issue_280", "issue_295", "issue_315"],
}
CASES = [case for cases in BATCHES.values() for case in cases]
BATCH_OF = {case: batch for batch, cases in BATCHES.items() for case in cases}
