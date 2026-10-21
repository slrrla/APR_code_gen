diag = [-1 if format(i, '03b') in targets else 1 for i in range(8)]
oracle = Diagonal(diag)
