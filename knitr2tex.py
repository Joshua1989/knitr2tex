import re, sys, os
from string import Template

def Rcode_to_Rnw(r_file, start_line=1, end_line=1, b_eval=True, show_head=0):
    lines = open(r_file).readlines()
    lines = lines[start_line-1:] if end_line==0 else lines[start_line-1:end_line]
    Rnw_str = Template(
    '''\\documentclass{article}
\\begin{document}
<<$range,warning=FALSE,message=FALSE,eval=$eval,echo=$echo>>=
$code_chunk
@
\\end{document}
    '''
    ).substitute(eval='TRUE' if b_eval else 'FALSE', 
                 echo='{0}:{1}'.format(show_head,end_line-start_line+1), 
                 range='line[{0}-line{1}]'.format(start_line,end_line),
                 code_chunk=''.join(lines))
    open("temp.Rnw", "w").write(Rnw_str)
    print("Rnw finished")
    os.system("Rscript -e \"knitr::knit('temp.Rnw', quiet=T)\"")
    print("knitr finished")

def prettify(code_file):
    lines = open("temp.tex").readlines()
    for i, line in enumerate(lines,1):
        L = re.split("((?<=.)\\\\(?:(?=usepackage)|(?=begin)).*?(?=(?:(?=\\\\usepackage)|(?=\\\\begin)|(?=\n))))",line)
        if len(L)>1 and "IfFileExists" not in line:
            lines[i-1] = "\n".join(list(filter(None, L)))    
    file_str = "".join(lines)
    # Find latex headers
    idx1 = list(re.finditer("\\\\usepackage", file_str))[0].start()
    idx2 = list(re.finditer("\\\\begin{document}", file_str))[0].start()
    RStyle_str = file_str[idx1:idx2]
    open("RStyle.tex", "w").write(RStyle_str)
    # Find first code chunk
    idx1 = list(re.finditer("\\\\begin{knitrout}", file_str))[0].start()
    idx2 = list(re.finditer("(?<=\\\\end{knitrout})", file_str))[0].start()
    Knitr_str = file_str[idx1:idx2]
    open(code_file, "w").write(Knitr_str)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        code_file = str(sys.argv[1])
        Rcode_to_Rnw(code_file)
        prettify(code_file.split(".")[0]+".tex")
        print(code_file.split(".")[0]+".tex")
    elif len(sys.argv) == 3:
        code_file, tex_file = str(sys.argv[1]), str(sys.argv[2])
        Rcode_to_Rnw(code_file)
        prettify(tex_file)
    elif len(sys.argv) == 5:
        code_file, tex_file = str(sys.argv[1]), str(sys.argv[2])
        start_line, end_line = int(sys.argv[3]), int(sys.argv[4])
        Rcode_to_Rnw(code_file, start_line, end_line)
        prettify(tex_file)
    elif len(sys.argv) == 6:
        code_file, tex_file = str(sys.argv[1]), str(sys.argv[2])
        start_line, end_line = int(sys.argv[3]), int(sys.argv[4])
        b_eval = int(sys.argv[5]) > 0
        Rcode_to_Rnw(code_file, start_line, end_line, b_eval)
        prettify(tex_file)
    elif len(sys.argv) == 7:
        code_file, tex_file = str(sys.argv[1]), str(sys.argv[2])
        start_line, end_line = int(sys.argv[3]), int(sys.argv[4])
        b_eval, show_head = int(sys.argv[5]) > 0, int(sys.argv[6])
        Rcode_to_Rnw(code_file, start_line, end_line, b_eval, show_head)
        prettify(tex_file)
    else:
        print("wrong argument format")
    os.system("rm -f temp.Rnw temp.tex")