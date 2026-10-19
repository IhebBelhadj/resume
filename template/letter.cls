% letter.cls: styling for generated cover letters. Reuses resume.cls (fonts, header,
% links) so the letter matches the resume, with letter margins and paragraph spacing.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{letter}[2026/10/19 Iheb Belhadj cover letter class]
\LoadClass{resume}

\geometry{top=1.5 cm, bottom=2 cm, left=2.5 cm, right=2.5 cm}
\setlength{\parskip}{0.8 em}

% date line and recipient block, after the header
\newcommand{\letterdate}[1]{\vspace{1 cm}{\raggedleft #1\par}\vspace{0.4 cm}}
\newcommand{\recipient}[1]{\textbf{#1}\par\vspace{0.4 cm}}

% body text: slightly larger than the resume, for reading
\newenvironment{letterbody}{\fontsize{11 pt}{15 pt}\selectfont}{\par}
