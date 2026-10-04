BATCHES = {
    1: ["issue_009", "issue_018_se", "issue_021_se", "issue_032_se", "issue_034",
        "issue_036", "issue_058_se", "issue_061", "issue_072", "issue_096"],
    2: ["issue_155", "issue_157", "issue_174", "issue_189", "issue_225",
        "issue_233", "issue_261", "issue_280", "issue_295", "issue_315"],
    3: ["issue_344", "issue_362", "issue_369", "issue_396", "issue_415",
        "issue_436", "issue_443", "issue_453", "issue_468", "issue_497"],
    4: ["issue_504", "issue_505", "issue_565", "issue_595", "issue_596",
        "issue_600", "issue_622", "issue_624", "issue_635", "issue_662"],
    5: ["issue_663", "issue_671", "issue_727", "issue_742", "issue_747",
        "issue_750", "issue_769", "issue_773", "issue_775", "issue_795"],
    6: ["issue_803", "issue_810", "issue_816", "issue_876", "issue_877",
        "issue_886", "issue_889", "issue_911", "issue_925", "issue_944"],
    7: ["issue_950", "issue_958", "issue_977", "issue_985", "issue_989",
        "issue_994", "issue_1035"],
}
CASES = [case for cases in BATCHES.values() for case in cases]
BATCH_OF = {case: batch for batch, cases in BATCHES.items() for case in cases}
