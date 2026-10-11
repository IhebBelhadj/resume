% resume.cls: all styling for generated resumes.
% Generated .tex files only call the environments/commands defined here;
% never put layout tweaks in generated files, change them here instead.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/10/11 Iheb Belhadj resume class]
\LoadClass[10pt, letterpaper]{article}

% Packages:
\RequirePackage[
ignoreheadfoot, % set margins without considering header and footer
top=.5 cm, % seperation between body and page edge from the top
bottom=.5 cm, % seperation between body and page edge from the bottom
left=1 cm, % seperation between body and page edge from the left
right=1 cm, % seperation between body and page edge from the right
footskip=1.0 cm, % seperation between body and footer
]{geometry} % for adjusting page geometry
\RequirePackage{titlesec} % for customizing section titles
\RequirePackage{tabularx} % for making tables with fixed width columns
\RequirePackage{array} % tabularx requires this
\RequirePackage[dvipsnames]{xcolor} % for coloring text
\definecolor{primaryColor}{RGB}{0, 0, 0} % define primary color
\RequirePackage{enumitem} % for customizing lists
\RequirePackage{fontawesome5} % for using icons
\RequirePackage{amsmath} % for math
\RequirePackage[
colorlinks=true,
urlcolor=primaryColor
]{hyperref} % for links, metadata and bookmarks
\RequirePackage{calc} % for calculating lengths
\RequirePackage{bookmark} % for bookmarks
\RequirePackage{changepage} % for one column entries (adjustwidth environment)
\RequirePackage{paracol} % for two and three column entries
\RequirePackage{needspace} % for avoiding page brake right after the section title
\RequirePackage{iftex} % check if engine is pdflatex, xetex or luatex

% Ensure that generate pdf is machine readable/ATS parsable:
\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage{lmodern}
\fi

\RequirePackage{charter}

% Some settings:
\raggedright
\AtBeginEnvironment{adjustwidth}{\partopsep0pt} % remove space before adjustwidth environment
\pagestyle{empty} % no header or footer
\setcounter{secnumdepth}{0} % no section numbering
\setlength{\parindent}{0pt} % no indentation
\setlength{\topskip}{0pt} % no top skip
\setlength{\columnsep}{0.15cm} % set column seperation
\pagenumbering{gobble} % no page numbering

\titleformat{\section}{\needspace{4\baselineskip}\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]

\titlespacing{\section}{
% left space:
  -1pt
}{
% top space:
  0.3 cm
}{
% bottom space:
  0.2 cm
} % section title spacing

\renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$} % custom bullet points
\newenvironment{highlights}{
  \begin{itemize}[
    topsep=0.10 cm,
    parsep=0.10 cm,
    partopsep=0pt,
    itemsep=0pt,
    leftmargin=0 cm + 10pt
    ]
  }{
\end{itemize}
}

\newenvironment{highlightsforbulletentries}{
  \begin{itemize}[
    topsep=0 cm,
    parsep=0.10 cm,
    partopsep=0pt,
    itemsep=0pt,
    leftmargin=10pt
    ]
  }{
\end{itemize}
} % new environment for highlights for bullet entries

\newenvironment{onecolentry}{
  \begin{adjustwidth}{
      0 cm + 0.00001 cm
    }{
      0 cm + 0.00001 cm
    }
  }{
  \end{adjustwidth}
} % new environment for one column entries

\newenvironment{twocolentry}[2][]{
  \onecolentry
  \def\secondColumn{#2}
  \setcolumnwidth{\fill, 4.5 cm}
  \begin{paracol}{2}
  }{
    \switchcolumn \raggedleft \secondColumn
  \end{paracol}
  \endonecolentry
} % new environment for two column entries

\newenvironment{header}{
  \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1}
}{
  \par\kern\topsep
} % new environment for the header

% separator between header contact items
\newsavebox\ANDbox
\sbox\ANDbox{$|$}
\newcommand{\AND}{\unskip
  \kern 5.0 pt%
  \cleaders\copy\ANDbox\hskip\wd\ANDbox
  \kern 5.0 pt%
  \ignorespaces
}

% --- High-level commands used by the generated .tex ---

% space between consecutive experience/education entries
\newcommand{\entryspace}{\vspace{0.2 cm}}
