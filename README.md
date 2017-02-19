# knitr2tex
A fast neat way to embed R source code as well as its output into LaTeX file

# Motivation
RStudio + knitr can create beautiful dynamic document in many languages, including LaTeX.
However, RStudio itself is not a good LaTeX editor, and thus I think it is useful to embed knitr into Sublime Text + LaTeXTools.

Most users create new build system for knitr to compile Rnw files, there are two drawbacks and inconviences:

1. Suppose you have a article contains a R code block that runs for a long time, each time you compile the whoe Rnw file you have to run that code again, but sometimes you want to run it only once and store the result for future compiling
2. Suppose you have a long article containing a lot math equations and R code blocks, if you use this build system and want to use backward search to jump from a math equation in PDF file to the corresponding line in the Rnw file, it will direct you to the tex file instead.

`knitr2tex` provides a solution for this problem, the basic idea is:

1. Given the R source file and line range, create a temporary Rnw file and use knitr to convert it into a tex file
2. I use python to split the tex file into two parts:
   * RStyle.tex: it contain all stylish macros for keyword highlighting
   * true content sub-tex file: it only contains the output of knitr for source code and its output, without LaTeX header, `\begin{docoment}` and `\end{document}`, so that in a tex file one can easily use `\input{}` command to incorporate this part.
3. The macros `\knitr` and `\smartknitr` uses `\immediate\write18` to run shell command, so when you compile the tex file, remember adding option `--shell-escape` to enable it. When you compile the tex file, it run shell command to call the python code, where in the python code it calls the R script to use knitr.

# Usage
At the tex file head, add
```
\IfFileExists{Rstyle.tex}{\input{Rstyle}}{}
\def\cmdPath{\detokenize{ knitr2tex.py }}
\def\knitr#1#2#3#4#5{
    \immediate\write18{python \cmdPath \detokenize{#1 #2 #3 #4 #5}}
    \input{#2}
}
\def\smartknitr#1#2#3#4#5{
    \IfFileExists{#2}{\input{#2}}{\knitr{#1}{#2}{#3}{#4}{#5}}
}
```
* For the `cmdPath`, if you put `knitr2tex.py` and your tex file in different directory, change it to where you store `knitr2tex.py`, notice that the spaces at beginging and end of the \detokenize command are necessary.
* `\knitr` command overwrite the previous output files whenever you compile; `\smartknitr` first check whether the target sub tex file exists, if it exists, then directly input it and do nothing else.
* The five arguments are
  1. directory of R source file
  2. directory of output sub tex file
  3. start line number of R source file
  4. end line number of R source file
  5. other options: first arg is whether to evaluate code, second arg is the start display line number
  
For example, `\smartknitr{test.R}{sub3.tex}{1}{15}{1 5}` it extracts the code from line 1 to line 15 in `test.R` and evaluates it.
On the display, it starts with line 5, which means only the code from line 5 to line 15, and the output of line 1 to line 15 are displayed in PDF file, but line 1 - line 4 are necessary for the code to be evaluated.

For more examples, please refer to `demo.tex`.
