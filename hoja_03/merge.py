def merge(fln1: str, fln2: str, res:str) -> None:
    with open(fln1) as f1, open(fln2) as f2, \
         open(res, 'w') as fres:
        l1 = f1.readline()
        l2 = f2.readline()
        while l1!='' and l2!='':
            n1 = int(l1)
            n2 = int(l2)
            if n1 < n2:
                fres.write(f'{n1}\n')
                l1 = f1.readline()
            else:
                fres.write(f'{n2}\n')
                l2 = f2.readline()
        while l1!='':
            n1 = int(l1)
            fres.write(f'{n1}\n')
            l1 = f1.readline()
        while l2!='':
            n2 = int(l2)
            fres.write(f'{n2}\n')
            l2 = f2.readline()
