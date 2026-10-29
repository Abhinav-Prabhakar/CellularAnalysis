"""Build the internship report in the template of the reference PDF."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import Engine, LEFT, RIGHT, WIDTH, TOP, BOTTOM  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures")
ASSETS = os.path.join(ROOT, "assets")
LOGO = os.path.join(ROOT, "report_assets", "snist_logo.png")

TITLE = "Link Performance Analysis of QPSK, 16-QAM and 64-QAM over an AWGN Channel"
DEPT = "ELECTRONICS AND COMMUNICATION ENGINEERING"

ANCHORS = {}
FIGPAGES = {}
FIGN = [0]
FIGCAPS = []


# ------------------------------------------------------------------ helpers
def chapter(e, label):
    e.new_page()
    e.text_at(LEFT, TOP, label, 16.86, 1)
    e.y = 97.9


def section(e, num, title, anchor=None):
    if e.y + 90 > BOTTOM:
        e.new_page()
    if anchor:
        ANCHORS[anchor] = e.page_no
    e.text_at(LEFT, e.y, num, 14.88, 1)
    e.text_at(118.1, e.y, title, 14.88, 1)
    e.y += 40.7


def subhead(e, title):
    if e.y + 60 > BOTTOM:
        e.new_page()
    e.para(title, size=12.57, leading=18, align="left", space_before=6, space_after=4)


def p(e, text, space_after=6.0, align="justify"):
    e.para(text, space_after=space_after, align=align)


def formula(e, text):
    e.para(text, align="center", space_before=4, space_after=10, last_left=False)


def bullets(e, items, num=False):
    for i, item in enumerate(items, 1):
        mark = f"{i}." if num else "•"
        if e.y + 22 > BOTTOM:
            e.new_page()
        y0 = e.y
        e.text_at(LEFT + (0 if num else 2), y0, mark, 12.57, 0)
        e.para(item, indent_first=22, indent_rest=22, space_after=4, align="left")


def figure(e, path, caption, width=380):
    FIGN[0] += 1
    n = FIGN[0]
    e.image(path, width, gap=10)
    if e.y + 60 > BOTTOM:
        e.new_page()
    e.para(f"**Figure – {n}:** {caption}", size=12, leading=16, align="center",
           width=WIDTH - 30, x0=LEFT + 15, space_before=8, space_after=18,
           last_left=False)
    FIGPAGES[n] = e.page_no
    FIGCAPS.append(caption)
    return n


def table(e, headers, rows, widths, caption=None, size=11.5):
    total = sum(widths)
    x0 = LEFT + (WIDTH - total) / 2

    def row_height(cells):
        return max(len(e.wrap(e.parse(str(c)), size, w - 12))
                   for c, w in zip(cells, widths)) * 16 + 3

    def paint(cells, ytop, bold=False):
        cx = x0
        height = 0
        for c, w in zip(cells, widths):
            words = e.parse(str(c))
            if bold:
                words = [[(t, 1, s) for (t, _st, s) in word] for word in words]
            lns = e.wrap(words, size, w - 12)
            height = max(height, len(lns) * 16 + 3)
            for i, ln in enumerate(lns):
                baseline = ytop + 2 + e.regular.ascender * size + i * 16
                e.draw_line(ln, baseline, size, align="center", x0=cx, width=w)
            cx += w
        return height

    if e.y + row_height(headers) + 8 + sum(row_height(r) for r in rows) + 40 > BOTTOM:
        e.new_page()
    e.y += 6
    e.line(e.y, x0, x0 + total, grey=0.25, width=0.7)
    e.y += 3
    e.y += paint(headers, e.y, bold=True)
    e.line(e.y, x0, x0 + total, grey=0.45, width=0.5)
    e.y += 2
    for row in rows:
        e.y += paint(row, e.y)
    e.line(e.y, x0, x0 + total, grey=0.25, width=0.7)
    e.y += 6
    if caption:
        if caption.startswith("Table") and ":" in caption:
            head, rest = caption.split(":", 1)
            caption = f"**{head}:**{rest}"
        e.para(caption, size=11.5, leading=15, align="center", space_before=4,
               space_after=14, last_left=False)
    else:
        e.y += 10


# --------------------------------------------------------------- front matter
def title_page(e, name, roll):
    e.new_page()
    e.text_at(297.7, 120.2, "Summer Industry Internship-I Report", 17.81, 1, align="center")
    e.text_at(297.7, 150.2, "(III Year I Semester)", 12.59, 1, align="center")
    e.text_at(297.7, 171.4, "on", 14.49, 0, align="center")
    e.y = 196.7
    e.para(f"“**{TITLE}**”", size=16.63, leading=20, align="center", width=WIDTH - 30,
           x0=LEFT + 15, space_after=0)
    e.text_at(297.7, 243.6, "*Submitted in the partial fulfilment of the requirements for*",
              14.58, 2, align="center")
    e.text_at(297.7, 268.4, "*the award of the degree of*", 14.58, 2, align="center")
    e.text_at(297.7, 292.7, "BACHELOR OF TECHNOLOGY", 16.08, 1, align="center")
    e.text_at(297.7, 319.5, "In", 14.86, 0, align="center")
    e.text_at(297.7, 344.1, DEPT, 16.08, 1, align="center")
    e.text_at(297.7, 370.7, "By", 14.86, 0, align="center")
    e.text_at(300.0, 400.0, name.upper(), 15.25, 1, align="right")
    e.text_at(330.0, 400.0, roll.upper(), 15.25, 1, align="left")
    e.text_at(297.7, 485.3, "UNDER THE GUIDANCE OF", 12.77, 1, align="center")
    e.text_at(297.7, 506.4, "T. Ramaswamy", 12.77, 1, align="center")
    e.text_at(297.7, 527.5, "Assistant Professor, Department of ECE", 12.77, 1, align="center")
    e.text_at(297.7, 548.9, "&", 12.77, 1, align="center")
    e.text_at(297.7, 569.8, "Dr. T. Swapna", 12.77, 1, align="center")
    e.text_at(297.7, 590.9, "Assistant Professor, Department of ECE", 12.59, 1, align="center")
    rect = (167.65, 630.25, 461.59, 663.5)
    e.page.insert_image(rect, filename=LOGO)
    e.text_at(297.7, 676.4, "DEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING",
              12.77, 1, align="center")
    e.text_at(297.7, 705.6, "SREENIDHI INSTITUTE OF SCIENCE AND TECHNOLOGY (A)",
              14.88, 1, align="center")
    e.text_at(297.7, 723.2, "Yamnampet (V), Ghatkesar (M), Hyderabad – 501 301.",
              12.59, 1, align="center")
    e.text_at(297.7, 738.6, "October 2026", 12.59, 1, align="center")


def certificate(e, name, roll):
    e.new_page()
    e.text_at(297.7, 81.9, "CERTIFICATE", 17.61, 1, align="center")
    e.y = 121.8
    e.para(
        "This is to certify that the Summer Industry Internship report entitled "
        f"**“{TITLE}”** is being submitted by **{name.upper()} ({roll.upper()})**, "
        "in partial fulfilment of the requirements for the award of **Bachelor of Technology** "
        "degree in **Electronics and Communication Engineering** to **Sreenidhi Institute of "
        "Science and Technology** affiliated to **Jawaharlal Nehru Technological University, "
        "Hyderabad** (Telangana). This record is a Bonafide work carried out by him under our "
        "guidance and supervision. The results embodied in the report have not been submitted "
        "to any other University or Institution for the award of any degree or diploma.",
        space_after=0)
    e.y = 415.0
    e.text_at(LEFT, 415.0, "Name of Internal Guide", 12.59, 1)
    e.text_at(LEFT, 436.1, "T. Ramaswamy", 12.75, 0)
    e.text_at(LEFT, 457.2, "Assistant Professor, Dept. of ECE", 11.80, 0)
    e.text_at(140.0, 476.7, "&", 12.75, 0)
    e.text_at(LEFT, 497.8, "Dr. T. Swapna", 13.11, 0)
    e.text_at(LEFT, 518.9, "Assistant Professor, Department of ECE", 12.75, 0)
    e.text_at(409.6, 613.0, "**Head of the Dept.**", 12.77, 1, align="center")
    e.text_at(409.6, 628.1, "Dr. S.P.V. SUBBA RAO", 13.11, 0, align="center")
    e.text_at(409.6, 643.3, "Professor & Head, Dept. of ECE", 12.75, 0, align="center")


def declaration(e, name, roll):
    e.new_page()
    e.text_at(297.7, 81.9, "DECLARATION", 17.61, 1, align="center")
    e.y = 121.8
    e.para(
        "I hereby declare that the work described in this Summer Industry Internship report "
        f"titled **“{TITLE}”** which is being submitted by me in partial fulfilment for the "
        "award of Bachelor of Technology in the Department of **Electronics and Communication "
        "Engineering**, Sreenidhi Institute of Science and Technology is the result of "
        "investigations carried out by me under the guidance of **T. Ramaswamy, Assistant "
        "Professor & Dr. T. Swapna, Assistant Professor, Sreenidhi Institute of Science and "
        "Technology, Hyderabad.**", space_after=14)
    e.para(
        "No part of this report is copied from books/ journals/ internet and whenever the "
        "portion is taken, the same has been duly referred. The report is based on the work "
        "carried out entirely by me and not copied from any other source. The work is original "
        "and has not been submitted for any Degree/Diploma of this or any other university.",
        space_after=40)
    e.text_at(LEFT, e.y, "Place: Hyderabad", 12.57, 0)
    e.y += 21.1
    e.text_at(LEFT, e.y, "Date:", 12.57, 0)
    e.text_at(435.0, 509.1, name.upper(), 12.0, 1, align="right")
    e.text_at(522.5, 509.1, roll.upper(), 12.0, 1, align="right")


def acknowledgements(e):
    e.new_page()
    e.text_at(297.7, 81.9, "ACKNOWLEDGEMENTS", 17.61, 1, align="center")
    e.y = 121.8
    p(e, "I wish to express my heartfelt acknowledgement to all those who have made it "
         "possible for me to carry out this project and submit this report.")
    p(e, "I would like to express my gratitude to **T. Ramaswamy & Dr. T. Swapna**, Assistant "
         "Professor, ECE Dept. for their training and guidance throughout this internship.")
    p(e, "I would like to extend my sincere thanks to the internship coordinator for motivating "
         "me to carry out this internship. It is my privilege to thank **Dr. S.P.V. SUBBA RAO**, "
         "HOD, Department of ECE, for his encouragement during the progress of this internship. "
         "I would like to express my deepest gratitude to our Principal **Dr. T. CH. SIVA REDDY**, "
         "and the Management for helping me develop self-perspective and work towards well defined "
         "goals.")
    p(e, "I would also like to thank my friends and family for being supportive all the time, "
         "and I am very much obliged to them.")


def abstract(e):
    e.new_page()
    ANCHORS["abstract"] = e.page_no
    e.text_at(LEFT, TOP, "ABSTRACT", 14.88, 1)
    e.y = 107.9
    p(e, "This report studies the link performance of three quadrature amplitude modulation "
         "schemes — QPSK, 16-QAM and 64-QAM — over an additive white Gaussian noise (AWGN) "
         "channel. The work is carried out as an interactive analysis tool that evaluates the "
         "bit error rate (BER), the symbol-to-noise ratio (E~s~/N~0~), the spectral efficiency "
         "and the error vector magnitude (EVM) of each scheme across an operating range of 0 to "
         "20 dB of energy per bit to noise power spectral density ratio (E~b~/N~0~).")
    p(e, "Each scheme is modelled as a Gray-coded square constellation normalised to unit "
         "average symbol energy. Bits are mapped to complex symbols, independent Gaussian noise "
         "is added to the in-phase and quadrature components, and the received samples are "
         "displayed as a scattering of points around the ideal constellation. The error "
         "probability is evaluated with the standard square-QAM approximation, and the required "
         "E~b~/N~0~ for a target BER is obtained by numerical bisection.")
    p(e, "The results reproduce the expected behaviour of uncoded QAM. At a BER of 10^−3^ the "
         "three schemes require 6.8 dB, 10.5 dB and 14.8 dB of E~b~/N~0~ respectively, so the "
         "two extra bits carried by 64-QAM cost about 8 dB of link margin compared with QPSK. "
         "Spectral efficiency grows from 2 to 6 bits per symbol over the same interval, and the "
         "error rate curves fall by roughly one decade for every additional 1.6 dB of SNR at "
         "the operating point. The constellation view makes the mechanism visible: at low SNR "
         "the received cloud of a 64-QAM signal spans several decision regions, while QPSK "
         "remains separable.")
    p(e, "The study therefore quantifies the central trade-off of adaptive modulation in 4G and "
         "5G links — throughput against robustness — and provides a reproducible, browser-based "
         "demonstration that runs on any machine without specialised software.")


def contents(e, prev_figs=None):
    e.new_page()
    ANCHORS["contents"] = e.page_no
    e.text_at(297.7, TOP, "**Contents**", 14.88, 1, align="center")
    e.y = 119.9
    entries = [
        ("Acknowledgements", "ack", 0), ("Abstract", "abstract", 0),
        ("Chapter-1  Introduction", None, 1),
        ("1.1  Motivation", "c1s1", 2), ("1.2  Problem Statement", "c1s2", 2),
        ("1.3  Objectives", "c1s3", 2), ("1.4  Digital Modulation in 4G and 5G", "c1s4", 2),
        ("1.5  Quadrature Amplitude Modulation", "c1s5", 2),
        ("Chapter-2  QAM Constellation and Signal Model", None, 1),
        ("2.1  What Is QAM", "c2s1", 2), ("2.2  Constellation Diagram and Gray Coding", "c2s2", 2),
        ("2.3  Symbol Energy and Normalisation", "c2s3", 2), ("2.4  Higher-Order QAM", "c2s4", 2),
        ("2.5  Spectral Efficiency and the Noise Penalty", "c2s5", 2),
        ("2.6  Advantages and Limitations", "c2s6", 2),
        ("Chapter-3  Software Environment", None, 1),
        ("3.1  Tools Used for the Analysis", "c3s1", 2),
        ("3.2  Why a Browser-Based Tool Was Used", "c3s2", 2),
        ("3.3  Structure of the Dashboard", "c3s3", 2),
        ("Chapter-4  Implementation", None, 1),
        ("4.1  Signal and Channel Model", "c4s1", 2), ("4.2  Constellation Rendering", "c4s2", 2),
        ("4.3  Bit Error Rate Computation", "c4s3", 2), ("4.4  Implementation Steps", "c4s4", 2),
        ("4.5  Interactive Controls and Readouts", "c4s5", 2),
        ("Chapter-5  Results and Discussion", None, 1),
        ("5.1  Output of the Dashboard", "c5s1", 2),
        ("5.2  Constellation Behaviour with Noise", "c5s2", 2),
        ("5.3  Bit Error Rate Results", "c5s3", 2),
        ("5.4  Spectral Efficiency and Required E~b~/N~0~", "c5s4", 2),
        ("5.5  Error Vector Magnitude", "c5s5", 2), ("5.6  Discussion", "c5s6", 2),
        ("Chapter-6", None, 1), ("6.1  Conclusion", "c6s1", 2),
        ("6.2  Future Scope", "c6s2", 2), ("6.3  References", "c6s3", 2),
        ("Annexure", "annex", 1),
    ]
    for label, key, level in entries:
        if e.y > BOTTOM - (60 if level == 1 else 20):
            e.new_page()
            e.y = TOP + 10
        if level == 1:
            e.y += 22.0
            e.text_at(LEFT, e.y, f"**{label}**", 12.59, 1)
            if key:
                e.text_at(484.7, e.y, str(ANCHORS.get(key, 0)), 12.59, 0, align="right")
            e.y += 22.1
        else:
            x = LEFT
            size = 12.57
            if level == 2:
                num, title = label.split("  ", 1)
                e.text_at(LEFT, e.y, num, size, 0)
                x = LEFT + 22.6
            else:
                title = label
            e.text_at(x, e.y, title, size, 0)
            page = ANCHORS.get(key, 0)
            e.text_at(484.7, e.y, str(page), size, 0, align="right")
            e.y += 22.1 if level == 0 else 14.1

    e.y += 26
    if e.y > BOTTOM - 120:
        e.new_page()
        e.y = TOP + 10
    ANCHORS["lof"] = e.page_no
    e.text_at(297.7, e.y, "**List of figures**", 16.0, 1, align="center")
    e.y += 44
    figs = prev_figs or []
    for i, cap in enumerate(figs, 1):
        if e.y > BOTTOM - 30:
            e.new_page()
            e.y = TOP + 10
        e.para(f"**Figure-{i}** : {cap}", size=12.2, leading=17, align="left")
        e.y += 6


# ------------------------------------------------------------------ chapters
def ch1(e):
    chapter(e, "Chapter-1 Introduction")
    section(e, "1.1", "Motivation", "c1s1")
    p(e, "Wireless networks are no longer judged only by coverage. A modern mobile link is asked "
         "to deliver video, cloud applications, industrial control traffic and billions of "
         "machine-type connections over a spectrum that is already fully occupied. Because the "
         "available bandwidth cannot be widened at will, the only remaining lever is spectral "
         "efficiency — the number of bits that can be carried per second in one hertz of "
         "spectrum. Every generation of cellular technology since 2G has been, in large part, a "
         "story of moving to denser modulation and better coding to raise that number.")
    p(e, "The modulation scheme is the component that converts this ambition into a physical "
         "waveform. Quadrature amplitude modulation (QAM) places several bits on a single radio "
         "carrier by combining two orthogonal carriers, one in phase and one in quadrature, each "
         "set to one of several amplitude levels. QPSK carries 2 bits per symbol, 16-QAM carries "
         "4 and 64-QAM carries 6. Each doubling of the constellation size doubles the throughput "
         "for the same symbol rate, which is why 64-QAM and 256-QAM are used whenever the radio "
         "conditions allow it.")
    p(e, "The gain is not free. As the constellation becomes denser the distance between "
         "neighbouring points shrinks, and the same amount of thermal noise pushes a received "
         "symbol across a decision boundary more often. A link that uses 64-QAM in poor "
         "conditions does not merely slow down — it fails, and the retransmissions that follow "
         "consume more resources than a robust QPSK transmission would have used. Real networks "
         "therefore link adaptation to channel quality: the base station measures the reported "
         "channel quality indicator and selects a modulation and coding scheme from a table, "
         "stepping down to QPSK at the cell edge and up to 64-QAM or 256-QAM close to the "
         "antenna.")
    p(e, "Understanding where those thresholds lie is the practical motivation for this work. "
         "The difference between the signal-to-noise ratio at which QPSK and 64-QAM reach the "
         "same error rate is the margin that link adaptation trades for throughput, and it is a "
         "number every radio engineer should be able to derive, plot and defend. This report "
         "builds that understanding from the constellation diagram upwards, and presents it as "
         "an interactive instrument rather than a static set of curves.")

    section(e, "1.2", "Problem Statement", "c1s2")
    p(e, "The performance of a digital link is usually quoted as a single curve — bit error rate "
         "against E~b~/N~0~ — but the comparison between modulation schemes is rarely made "
         "explicit. Textbook treatments derive the error probability for each scheme separately, "
         "often with different normalisations, and the reader is left to reconstruct the "
         "trade-off. In a laboratory, the same comparison requires a vector signal generator, a "
         "noise source and a receiver, which is beyond the scope of a short project.")
    p(e, "The problem addressed here is therefore twofold. First, the three schemes must be "
         "placed on a common footing: unit average symbol energy, Gray-coded square "
         "constellations, and an identical AWGN channel, so that the only variable is the "
         "constellation size. Second, the result must be presented in a form that shows both the "
         "mechanism and the number — the received constellation that explains *why* 64-QAM fails "
         "first, and the error-rate curve that quantifies *when* it fails. A tool that a student "
         "or an engineer can open in a browser and sweep through the operating range satisfies "
         "both requirements without laboratory hardware.")

    section(e, "1.3", "Objectives", "c1s3")
    p(e, "The objectives of the present work are:", space_after=4)
    bullets(e, [
        "To model QPSK, 16-QAM and 64-QAM as Gray-coded square constellations with unit average "
        "symbol energy, so that the three schemes can be compared on an identical basis.",
        "To simulate the effect of an additive white Gaussian noise channel on the received "
        "symbols and to visualise the resulting spread around each ideal constellation point.",
        "To compute the bit error rate of each scheme over an E~b~/N~0~ range of 0 to 20 dB and "
        "to determine, by numerical inversion, the E~b~/N~0~ required to reach target error "
        "rates of 10^−2^, 10^−3^ and 10^−4^.",
        "To relate the spectral efficiency of each scheme to its noise penalty, and to express "
        "the result as a link-budget margin that can be used in modulation and coding scheme "
        "selection.",
        "To implement the complete analysis as a self-contained, interactive browser "
        "application, and to verify that its numerical output agrees with the accepted "
        "theoretical expressions for square QAM.",
    ], num=True)

    section(e, "1.4", "Digital Modulation in 4G and 5G", "c1s4")
    p(e, "Long Term Evolution (LTE) uses QPSK, 16-QAM and 64-QAM on both the downlink and the "
         "uplink, with 256-QAM added for the downlink in later releases. The 5G New Radio (NR) "
         "specification extends the set to QPSK, 16-QAM, 64-QAM and 256-QAM for the downlink and, "
         "from Release 16 onwards, 64-QAM and 256-QAM for the uplink, together with π/2-BPSK for "
         "low-power transmission. The choice is not made per cell but per transmission: the "
         "scheduler selects an index from a modulation and coding table, and that index fixes "
         "both the constellation and the channel code rate.")
    figure(e, os.path.join(FIG, "fig_generations.png"),
           "Evolution of mobile communication generations and the modulation schemes associated "
           "with each of them.", width=430)
    p(e, "The progression in the figure is not accidental. Each generation inherited the "
         "constellation of its predecessor and added a denser one for users with a good channel. "
         "The practical consequence is that a 5G cell does not have a single data rate; it has a "
         "distribution of rates that depends on how far each user is from the antenna and how "
         "much interference the user experiences. Link adaptation walks up and down this "
         "distribution several hundred times per second.")
    p(e, "This is also why the error-rate curves of the individual constellations matter more "
         "than the peak rates quoted in marketing material. The operating point of a real link "
         "sits a fixed margin above the E~b~/N~0~ at which the chosen scheme reaches an "
         "acceptable block error rate — typically one percent after coding. The uncoded curves "
         "computed in this report are the reference from which that margin is measured.")

    section(e, "1.5", "Quadrature Amplitude Modulation", "c1s5")
    p(e, "QAM transmits information on two carriers of the same frequency that are in phase "
         "quadrature, that is, separated by ninety degrees. Because the two carriers are "
         "orthogonal over a symbol interval, they can be separated at the receiver without "
         "interference, and each may carry an independent amplitude. The transmitted symbol is "
         "conveniently written as a complex number whose real part is the in-phase amplitude I "
         "and whose imaginary part is the quadrature amplitude Q.")
    formula(e, "s(t) = I·cos(2πf~c~t) − Q·sin(2πf~c~t)  =  Re{ (I + jQ)·exp(j2πf~c~t) }")
    p(e, "A constellation of M symbols therefore occupies M points in the I–Q plane, and each "
         "point carries k = log~2~M bits. When M is a perfect square and the points are arranged "
         "on a regular grid, the scheme is called square QAM; QPSK, 16-QAM and 64-QAM are the "
         "square cases with M = 4, 16 and 64. Square constellations are used almost universally "
         "in practice because they can be generated by two independent pulse amplitude modulators "
         "and because their decision boundaries are simple vertical and horizontal lines.")
    p(e, "The rest of this report treats the link in complex baseband. The carrier is removed "
         "analytically, the symbol is represented by the complex number I + jQ, and the channel "
         "adds a complex Gaussian sample whose real and imaginary parts are independent and "
         "identically distributed. This is the standard equivalent model for a linear AWGN "
         "channel and it keeps the analysis independent of the carrier frequency, which is what "
         "allows a single set of curves to describe an LTE link at 2 GHz and an NR link at 28 GHz "
         "alike.")
    p(e, "At the receiver the process is reversed. Coherent detection multiplies the incoming "
         "waveform by locally generated in-phase and quadrature carriers, and the two matched "
         "filters are sampled once per symbol interval. The pair of samples is the received "
         "complex symbol, and the decision is taken by assigning it to the nearest point of the "
         "constellation. Everything that follows in this report is a property of that one "
         "geometric operation: the noise displaces the sample, the decision regions partition the "
         "plane, and the error rate counts the fraction of samples that cross a boundary.")


def ch2(e):
    chapter(e, "Chapter-2 QAM Constellation and Signal Model")
    section(e, "2.1", "What Is QAM", "c2s1")
    p(e, "Quadrature amplitude modulation combines two ideas: amplitude modulation of two "
         "orthogonal carriers, and the mapping of a group of bits onto the resulting pair of "
         "amplitudes. If the in-phase amplitude takes one of √M levels and the quadrature "
         "amplitude takes one of √M levels, the Cartesian product gives M distinct symbols and "
         "therefore log~2~M bits per symbol interval. The symbol rate is unchanged; only the "
         "number of distinguishable states grows.")
    p(e, "For a square constellation with M points the levels are symmetrically placed about the "
         "origin. With the points indexed by i and j running from 0 to √M − 1, the normalised "
         "coordinates used throughout this work are:")
    formula(e, "I~i~ = (2i − (√M − 1)) / √(2(M − 1)/3)")
    formula(e, "Q~j~ = (2j − (√M − 1)) / √(2(M − 1)/3)")
    p(e, "The divisor is chosen so that the average symbol energy is unity, E[|s|^2^] = 1. This "
         "normalisation is what makes the comparison fair: at a given E~b~/N~0~ every scheme "
         "delivers the same energy per information bit, and the only difference that remains is "
         "how densely the symbols are packed into the plane.")
    p(e, "Two quantities describe the constellation geometrically. The minimum distance d is the "
         "spacing between adjacent points along either axis, and the average symbol energy E~s~ "
         "is the mean squared distance from the origin. For square QAM they are related by:")
    formula(e, "E~s~ = (M − 1)·d^2^/6,    that is,   d = √(6E~s~/(M − 1))")
    p(e, "As M grows, d shrinks for a fixed E~s~: the points crowd together and the same noise "
         "variance produces a larger number of boundary crossings. Every property of QAM "
         "performance follows from this single geometric fact.")

    section(e, "2.2", "Constellation Diagram and Gray Coding", "c2s2")
    p(e, "The assignment of bit patterns to constellation points is called labelling, and it is "
         "not arbitrary. With natural binary labelling, two points that are physically adjacent "
         "may differ in several bit positions, so a single symbol error corrupts several bits. "
         "Gray coding removes this effect by ensuring that any two adjacent points differ in "
         "exactly one bit. A symbol error caused by noise pushing the received sample into a "
         "neighbouring decision region then produces, with high probability, a single bit error.")
    p(e, "Square QAM admits a particularly simple Gray labelling: the bits along the in-phase "
         "axis are Gray-coded independently of the bits along the quadrature axis, and the "
         "in-phase bits are transmitted as the most significant half of the label. The result is "
         "a constellation in which the label of a point changes by one bit as the point moves one "
         "step horizontally or vertically, but by two or more bits along a diagonal — and "
         "diagonal transitions are much less likely because they require a larger noise "
         "excursion.")
    figure(e, os.path.join(FIG, "fig_qpsk.png"),
           "QPSK constellation. Each symbol carries two bits and the four decision regions are "
           "the four quadrants.", width=250)
    p(e, "The three constellations used in this report are shown in the figures that follow. "
         "QPSK is the degenerate case in which the amplitude of each carrier is either positive "
         "or negative; its decision boundaries are the two axes, and the minimum distance is "
         "large relative to the symbol energy. This is why QPSK survives conditions in which the "
         "denser schemes have already collapsed.")
    figure(e, os.path.join(FIG, "fig_16qam.png"),
           "16-QAM constellation. Four bits per symbol, with Gray-coded labels on a 4 × 4 grid.",
           width=250)
    figure(e, os.path.join(FIG, "fig_64qam.png"),
           "64-QAM constellation. Six bits per symbol on an 8 × 8 grid; the minimum distance is "
           "half that of 16-QAM at the same symbol energy.", width=250)
    p(e, "Comparing the three figures at a glance shows the price of spectral efficiency. At the "
         "same average symbol energy, the minimum distance of 16-QAM is 1/√5 of that of QPSK, and "
         "the minimum distance of 64-QAM is a further factor of two smaller. Noise that is "
         "harmless to QPSK is therefore sufficient to move a 64-QAM sample into a neighbouring "
         "cell, which is exactly the behaviour observed in the constellation panel of the "
         "dashboard.")

    section(e, "2.3", "Symbol Energy and Normalisation", "c2s3")
    p(e, "The energy per symbol E~s~ and the energy per bit E~b~ are related by E~s~ = k·E~b~, "
         "because each symbol carries k bits. In decibels this becomes the relation used "
         "throughout the analysis:")
    formula(e, "E~s~/N~0~ (dB) = E~b~/N~0~ (dB) + 10·log~10~k")
    p(e, "For QPSK the offset is 3.0 dB, for 16-QAM 6.0 dB and for 64-QAM 7.8 dB. The offset is "
         "the reason a 64-QAM receiver needs a much cleaner symbol to achieve the same bit error "
         "rate: the noise is spread over six bits rather than two, so each bit receives only a "
         "sixth of the symbol energy.")
    p(e, "In the noise model used here, the complex channel adds a sample whose real and "
         "imaginary parts are independent Gaussian variables, each with variance N~0~/2. With "
         "unit symbol energy the standard deviation per dimension is therefore:")
    formula(e, "σ = √(N~0~/2) = 1/√(2·E~s~/N~0~)")
    p(e, "This is the expression implemented in the dashboard when it draws the received "
         "samples. It also fixes the relationship between the signal-to-noise ratio quoted in a "
         "link budget and the spread of the cloud: a 6 dB improvement in E~s~/N~0~ halves the "
         "standard deviation and therefore halves the radius of the visible cloud.")

    section(e, "2.4", "Higher-Order QAM", "c2s4")
    p(e, "The progression from QPSK to 16-QAM to 64-QAM does not change the transmitted "
         "bandwidth. All three schemes occupy the same channel and use the same symbol rate; they "
         "differ only in how many bits each symbol carries. Doubling the number of bits per "
         "symbol doubles the throughput at the cost of halving the spacing between adjacent "
         "points in each dimension, which is why the error-rate curves shift to the right by "
         "roughly three decibels of E~s~/N~0~ for every additional bit.")
    p(e, "The relationship is visible in the analytic expression for the bit error rate of "
         "square QAM, which is derived from the tail probability of the Gaussian distribution and "
         "the geometry of the decision regions:")
    formula(e, "BER ≈ (4/k)·(1 − 1/√M)·Q( √( 3k·E~b~/N~0~ / (M − 1) ) )")
    p(e, "Here Q(·) is the Gaussian tail probability, k = log~2~M, and the factor 4/k accounts "
         "for the two dimensions and the average number of bit errors per symbol error under "
         "Gray labelling. The expression is an upper bound for Gray-coded square QAM and becomes "
         "tight at error rates below about 10^−2^, which is the region of practical interest.")
    p(e, "Two features of the expression deserve emphasis. First, the argument of Q(·) depends on "
         "E~b~/N~0~ multiplied by k, so for a fixed E~b~/N~0~ the effective argument shrinks as M "
         "grows — the constellation is more sensitive, not less. Second, the prefactor (1 − "
         "1/√M) approaches unity for large M, so the curves become parallel at low error rates "
         "and the horizontal distance between them is the penalty for the extra bits.")

    section(e, "2.5", "Spectral Efficiency and the Noise Penalty", "c2s5")
    p(e, "Spectral efficiency is the number of information bits delivered per second per hertz "
         "of bandwidth. For an uncoded single-carrier link it is simply k bits per symbol times "
         "the symbol rate, divided by the occupied bandwidth, which for a Nyquist-limited system "
         "reduces to k bit/s/Hz. QPSK therefore achieves 2 bit/s/Hz, 16-QAM 4 bit/s/Hz and "
         "64-QAM 6 bit/s/Hz, before any channel coding is applied.")
    p(e, "Shannon's capacity theorem places an upper bound on what any system can achieve at a "
         "given signal-to-noise ratio, with bandwidth-normalised capacity C/B = log~2~(1 + SNR). "
         "Uncoded QAM operates several decibels below this bound, and the gap grows with the "
         "constellation size; coded systems recover most of the difference. For the comparison in "
         "this report the uncoded curves are the relevant reference, because they isolate the "
         "effect of the constellation itself.")
    p(e, "The size of the gap is easy to state at the operating points reported in Chapter 5. "
         "QPSK reaches a bit error rate of 10^−3^ at 9.8 dB of E~s~/N~0~, where the Shannon "
         "limit is 3.4 bit/s/Hz against the 2 bit/s/Hz actually delivered. 16-QAM at 16.5 dB "
         "sits at 5.5 bit/s/Hz against 4, and 64-QAM at 22.6 dB sits at 7.5 bit/s/Hz against 6. "
         "The shortfall is between 1.4 and 1.5 bit/s/Hz in all three cases, and closing it is "
         "the task of the channel code rather than of the constellation.")
    figure(e, os.path.join(FIG, "fig_ber.png"),
           "Bit error rate against E~b~/N~0~ for the three schemes. Markers show the operating "
           "points at a BER of 10^−3^.", width=400)
    p(e, "The curves in the figure show the characteristic waterfall shape of an AWGN link. At "
         "low E~b~/N~0~ the error rate is dominated by the Gaussian tail and falls slowly; once "
         "the argument of the Q-function exceeds about two, the decay becomes exponential in the "
         "ratio and the curve is almost a straight line on a logarithmic axis. The horizontal "
         "separation between the curves is the link margin that adaptive modulation consumes "
         "when it steps to a denser constellation.")
    p(e, "It is worth stating the trade-off in the units a link budget uses. Moving from QPSK to "
         "16-QAM doubles the throughput and, at a BER of 10^−3^, requires 3.7 dB more E~b~/N~0~. "
         "Moving from 16-QAM to 64-QAM adds another 4.3 dB for a further fifty percent of "
         "throughput. In E~s~/N~0~ terms the cost is close to three decibels per additional bit, "
         "which is the number that appears in every discussion of modulation and coding scheme "
         "selection.")

    section(e, "2.6", "Advantages and Limitations", "c2s6")
    p(e, "The advantages of QAM are well established and explain its use in every modern "
         "cellular standard:", space_after=3)
    bullets(e, [
        "High spectral efficiency: several bits are carried per symbol without additional "
        "bandwidth, and the efficiency grows logarithmically with the constellation size.",
        "Simple implementation: square constellations separate into two independent pulse "
        "amplitude modulators and demodulators, one per axis.",
        "Graceful adaptation: the family QPSK, 16-QAM, 64-QAM and 256-QAM shares one receiver "
        "architecture, so a terminal can change scheme from one subframe to the next.",
        "Compatibility with coding: Gray labelling keeps the bit error rate close to "
        "SER/log~2~M, which allows binary codes to be used directly on the bit stream.",
    ])
    p(e, "The limitations follow from the same geometry:", space_after=3)
    bullets(e, [
        "Sensitivity to noise: the required E~b~/N~0~ rises steeply with M, so dense "
        "constellations are usable only close to the base station.",
        "Sensitivity to amplitude distortion: any nonlinearity in the power amplifier or any "
        "residual gain error in the receiver distorts the outer points of the constellation "
        "first.",
        "Sensitivity to phase noise and frequency offset: a rotation of the constellation by a "
        "few degrees is enough to move outer points across a decision boundary.",
        "Peak-to-average power ratio: dense constellations with many amplitude levels require "
        "larger back-off in the amplifier, which reduces the average transmit power.",
    ])
    p(e, "The AWGN model used in this report isolates the first of these limitations. It is the "
         "correct starting point, because the noise penalty sets the floor on E~b~/N~0~ below "
         "which no amount of equalisation will help, and because every other impairment is "
         "measured against it as an implementation margin.")
    p(e, "The impairments are not independent. The amplitude levels that raise the peak-to-average "
         "ratio also make the outer ring of the constellation the first casualty of amplifier "
         "compression, and the sensitivity to phase noise grows with the radius of that ring. In "
         "a complete link budget the four effects are therefore lumped into a single "
         "implementation margin added to the AWGN requirement, and the design target is to keep "
         "that margin small enough that the densest supported constellation stays usable over the "
         "intended coverage area.")


def ch3(e):
    chapter(e, "Chapter-3 Software Environment")
    section(e, "3.1", "Tools Used for the Analysis", "c3s1")
    p(e, "The analysis is implemented as a single-page web application. The structural layer is "
         "HTML5, the presentation layer is CSS3 and the computational layer is ECMAScript 2015 "
         "JavaScript. All graphics are drawn on HTML canvas elements with the two-dimensional "
         "context, and the animation is driven by requestAnimationFrame. No library, build step "
         "or server is required: the file opens directly in a browser and all computation happens "
         "on the client.")
    p(e, "The numerical work uses only the JavaScript Math object. The complementary error "
         "function is evaluated with the rational approximation of Numerical Recipes, which "
         "attains a relative error below 1.2 × 10^−7^ over the range of interest; the Gaussian "
         "tail probability Q(x) follows from erfc(x/√2). Normal random samples are generated "
         "with the Box–Muller transform, with the second variate cached so that each pair of "
         "uniform deviates produces two independent Gaussian samples.")
    p(e, "This report was produced with a different set of tools: the figures were generated "
         "with Python and Matplotlib from the same equations that the dashboard evaluates, so "
         "that the printed curves can be checked against the interactive ones. The agreement "
         "between the two is one of the consistency checks reported in Chapter 5.")

    section(e, "3.2", "Why a Browser-Based Tool Was Used", "c3s2")
    p(e, "MATLAB is the conventional environment for link-level simulation, and the reference "
         "implementation of this study could have been written in it. A browser implementation "
         "was preferred for reasons that matter in a teaching context. First, there is nothing to "
         "install: the tool runs on a laboratory machine, a personal laptop or a phone, which "
         "removes the licence and toolchain problems that otherwise consume a large part of a "
         "short project.")
    p(e, "Second, the visual feedback is immediate and continuous. The constellation panel is "
         "redrawn roughly fourteen times per second, so dragging the E~b~/N~0~ slider produces a "
         "smooth change in the cloud rather than a sequence of static plots. Seeing a 64-QAM "
         "constellation dissolve into overlapping clusters at 4 dB communicates the mechanism "
         "far more effectively than the corresponding number in a table.")
    p(e, "Third, the result is reproducible and shareable. The complete application is a single "
         "text file of about nine hundred lines, it can be published as a static page, and its "
         "numerical output can be verified by reading the source. There is no hidden toolbox "
         "function between the equation and the curve.")

    section(e, "3.3", "Structure of the Dashboard", "c3s3")
    p(e, "The interface is organised into three regions. A control strip at the top carries the "
         "E~b~/N~0~ slider and its current value. A row of three constellation cards shows the "
         "received symbols of each scheme together with its bit error rate and symbol-to-noise "
         "ratio. A lower row combines the error-rate chart with a panel of derived quantities: "
         "the spectral efficiency of each scheme and the E~b~/N~0~ it requires for a bit error "
         "rate of 10^−3^.")
    table(e,
          ["Region", "Elements", "Quantity displayed"],
          [["Control", "Slider, value readout", "E~b~/N~0~, 0 – 20 dB"],
           ["Constellation", "Three canvases", "I/Q scatter, BER, E~s~/N~0~"],
           ["Analysis", "Curve chart", "BER against E~b~/N~0~"],
           ["Summary", "Bars and table", "Spectral efficiency, required E~b~/N~0~"]],
          [90, 150, 190],
          caption="Table 1: Functional regions of the dashboard.")
    p(e, "The layout is responsive. On a narrow screen the three constellation cards stack "
         "vertically and the analysis row becomes a single column, so the same instrument can be "
         "used on a phone without loss of function. The canvas resolution follows the device "
         "pixel ratio, capped at two, so that the plot remains sharp on high-density displays "
         "without excessive drawing cost.")
    p(e, "Behind the interface the code is divided into four functions that mirror the signal "
         "path: buildConstellation() creates the normalised points for a given M, receive() adds "
         "the Gaussian samples, berOf() evaluates the analytic error probability, and "
         "requiredEbn0() inverts it for a target rate. The three scheme objects in the SCHEMES "
         "array carry their own canvas, readout elements and colour, so the update loop is a "
         "single forEach over that array with no per-scheme branching. This is what allows a new "
         "constellation to be added by appending one entry rather than by editing the drawing "
         "code.")


def ch4(e):
    chapter(e, "Chapter-4 Implementation")
    section(e, "4.1", "Signal and Channel Model", "c4s1")
    p(e, "The transmitter model consists of a uniform random bit source, a Gray-coded symbol "
         "mapper and a complex baseband channel. For each scheme the mapper generates the "
         "constellation once at start-up, using the normalisation of Section 2.1, and stores the "
         "coordinates of M points. A transmitted symbol is drawn uniformly from this set, which "
         "corresponds to equiprobable data.")
    figure(e, os.path.join(FIG, "fig_system.png"),
           "Block diagram of the simulated baseband link. The channel adds complex Gaussian noise "
           "of variance N~0~/2 per dimension.", width=430)
    p(e, "The channel adds independent Gaussian noise to each coordinate. For a given "
         "E~b~/N~0~ the symbol-to-noise ratio follows from the number of bits per symbol, and the "
         "standard deviation per dimension is obtained from the expression of Section 2.3. In "
         "code, the sequence is two lines:", space_after=0)
    _l1 = "const esn0  = Math.pow(10, (ebn0 + 10 * Math.log10(k)) / 10);"
    _l2 = "const sigma = 1 / Math.sqrt(2 * esn0);"
    _x = (LEFT + RIGHT) / 2 - e.mono.text_length(_l1, 10.2) / 2
    e.code_line(_l1, space_before=8, space_after=0, x0=_x)
    e.code_line(_l2, space_before=0, space_after=10, x0=_x)
    p(e, "The receiver is represented analytically rather than symbol by symbol. Because the "
         "channel is memoryless and the symbols are equiprobable, the bit error rate is fully "
         "determined by the Gaussian tail probability at the decision threshold, and the "
         "dashboard evaluates that closed form rather than counting errors from a finite sample. "
         "This choice removes the statistical noise of a Monte Carlo estimate — at 10^−6^ a "
         "direct simulation would require billions of symbols to produce a stable count — while "
         "the constellation panel still uses explicit random samples, because there the visual "
         "spread is the point.")

    section(e, "4.2", "Constellation Rendering", "c4s2")
    p(e, "Each constellation card holds a square canvas that is sized to the device pixel ratio "
         "on every repaint. The coordinate transform maps the complex plane onto the canvas so that "
         "the full range ±1.55 is visible, which leaves a margin around the outermost points for "
         "the noise cloud to expand into at low signal-to-noise ratios.")
    p(e, "The received samples are generated by taking each ideal point in turn and adding a "
         "Gaussian deviate to each coordinate. The number of samples per point is chosen so that "
         "about 260 points are drawn in total, with a floor of three samples per point so that "
         "even 64-QAM shows a visible cloud. The samples are drawn first, at thirty percent "
         "opacity, and the ideal constellation is drawn on top as white-filled circles with a "
         "coloured outline. The result is a cloud whose density and radius encode the noise "
         "level while the ideal grid remains legible underneath.")
    p(e, "The panel is repainted on a timer of about seventy milliseconds rather than on every "
         "animation frame. At sixty frames per second the eye cannot follow individual samples, "
         "and the slower refresh keeps the processor load low enough to leave the slider "
         "responsive. When the slider moves, the new value takes effect on the next repaint, so "
         "the cloud appears to breathe as the noise level changes.")

    section(e, "4.3", "Bit Error Rate Computation", "c4s3")
    p(e, "The bit error rate is evaluated from the standard approximation for Gray-coded square "
         "QAM. The complementary error function is computed with the polynomial approximation, "
         "the Q-function follows by scaling, and the result is multiplied by the geometric "
         "prefactor of Section 2.4. The same function is used for all three schemes, with M and k "
         "passed as arguments, so the three curves are guaranteed to be computed on an identical "
         "basis.")
    p(e, "The inverse problem — finding the E~b~/N~0~ at which a scheme reaches a given error "
         "rate — is solved by bisection on the interval from −10 dB to 40 dB. Sixty iterations "
         "reduce the bracket to far below the precision of the display, and the monotonicity of "
         "the error function guarantees convergence. The three required values shown in the "
         "summary panel, and in the results table of Chapter 5, are produced by this routine "
         "rather than typed in by hand.")
    p(e, "Two display conventions are worth noting. The chart floor is fixed at 10^−7^ so that "
         "the curves are not compressed at high E~b~/N~0~; markers that fall below the floor are "
         "drawn as hollow circles at the axis, which signals that the true value is lower than "
         "the plot can resolve. Error rates are printed in scientific notation with superscript "
         "exponents, and values that underflow the double-precision range are printed as a dash "
         "rather than as zero.")

    section(e, "4.4", "Implementation Steps", "c4s4")
    p(e, "The implementation follows the signal path in order. Each step corresponds to a "
         "function or a block in the source listed in the Annexure.", space_after=3)
    bullets(e, [
        "**Generate data.** A uniform random bit stream is produced for the selected scheme, "
        "with k bits per symbol.",
        "**Map to symbols.** The bits are grouped in blocks of k and mapped to the Gray-coded "
        "constellation point with the corresponding index, normalised to unit average energy.",
        "**Scale the symbol.** The constellation is held at unit energy; the operating point is "
        "carried by the noise variance rather than by the signal amplitude.",
        "**Add AWGN.** Independent Gaussian deviates are added to the in-phase and quadrature "
        "components, each with standard deviation σ = 1/√(2·E~s~/N~0~).",
        "**Display the received samples.** The complex samples are projected onto the canvas and "
        "drawn under the ideal constellation.",
        "**Evaluate the error probability.** The analytic BER is computed for the current "
        "E~b~/N~0~ and displayed on the card, together with the corresponding E~s~/N~0~.",
        "**Plot the curves.** The error rate of each scheme is evaluated over 0–20 dB and drawn "
        "on a logarithmic axis with the current operating point marked.",
        "**Invert for the target error rate.** Bisection gives the E~b~/N~0~ required for a BER "
        "of 10^−3^, and the difference from the QPSK baseline is displayed as a margin.",
        "**Update on interaction.** The slider event recomputes the readouts and the chart "
        "immediately, while the constellation panel refreshes on its own timer.",
    ], num=True)

    section(e, "4.5", "Interactive Controls and Readouts", "c4s5")
    p(e, "The only input is a single slider covering 0 to 20 dB in steps of 0.1 dB. The range was "
         "chosen so that it contains the interesting part of all three curves: QPSK is already "
         "below 10^−4^ at 10 dB, while 64-QAM only reaches 10^−3^ at about 14.8 dB. A single "
         "control keeps the instrument simple and makes the coupling between the panels obvious.")
    p(e, "Each constellation card reports the bit error rate and the symbol-to-noise ratio for "
         "its scheme at the current setting, so that the reason for the difference between the "
         "cards is visible in numbers as well as in the drawing. The summary panel reports the "
         "spectral efficiency and the required E~b~/N~0~, with the QPSK requirement as the "
         "baseline. The three pieces together answer the questions a link-budget calculation "
         "asks: how many bits per symbol, at what noise level, with what margin.")
    p(e, "Numerical readouts follow fixed conventions so that values from different operating "
         "points can be compared without reinterpretation. Error rates are printed in the form "
         "2.7 × 10^−2^ with two significant figures and a true superscript exponent, values "
         "below the smallest representable double are printed as a dash rather than as zero, "
         "and the symbol-to-noise ratio is rounded to one decimal place. The required "
         "E~b~/N~0~ values in the summary card carry one decimal and a signed margin relative "
         "to the QPSK baseline, so the cost of each constellation is read directly as +3.7 dB "
         "and +8.0 dB.")
    p(e, "The summary card is computed once when the page loads, because the E~b~/N~0~ "
         "required for a target error rate is a property of the constellation and not of the "
         "current slider position. The constellation cards and the curve chart, by contrast, "
         "are recomputed on every input event. This split keeps the interaction cheap: moving "
         "the slider redraws three scatter plots and one chart, while the bisection that "
         "produces the summary is performed three times in total.")
    p(e, "Rendering is kept stable across displays. Every canvas is resized to the CSS pixel "
         "size multiplied by the device pixel ratio, capped at two, before each repaint, and "
         "the drawing code works in CSS pixels after a corresponding transform. A resize "
         "event is debounced by 120 ms so that dragging a window edge does not trigger a "
         "burst of redraws, and the constellation timer runs at about seventy milliseconds "
         "independently of the slider. The result is a panel that remains sharp on a "
         "high-density screen and responsive on a modest laptop.")


def ch5(e):
    chapter(e, "Chapter-5 Results and Discussion")
    section(e, "5.1", "Output of the Dashboard", "c5s1")
    p(e, "The figure below shows the complete dashboard at the default operating point of 10 dB. "
         "All three constellations are separable, but the difference in margin is already "
         "visible: the QPSK cloud is compact, the 16-QAM cloud fills a noticeable fraction of "
         "each cell, and the 64-QAM cloud has begun to touch the boundaries between adjacent "
         "points.")
    figure(e, os.path.join(ASSETS, "hero.png"),
           "The interactive link-performance dashboard at E~b~/N~0~ = 10 dB.", width=455)
    p(e, "The numerical readouts at this operating point are 3.9 × 10^−6^ for QPSK, 1.8 × 10^−3^ "
         "for 16-QAM and 2.7 × 10^−2^ for 64-QAM. The corresponding symbol-to-noise ratios are "
         "13.0 dB, 16.0 dB and 17.8 dB, the offsets of 3.0, 6.0 and 7.8 dB predicted by "
         "E~s~/N~0~ = E~b~/N~0~ + 10·log~10~k. The values agree with a direct evaluation of the "
         "analytic expression to the precision of the display.")

    section(e, "5.2", "Constellation Behaviour with Noise", "c5s2")
    p(e, "Lowering the slider to 4 dB produces the second figure. The QPSK symbols remain clearly "
         "separated — the cloud radius is still small compared with the distance between "
         "neighbouring points — while the 64-QAM constellation has lost its structure completely: "
         "the individual clouds overlap and the eye can no longer assign samples to cells. The "
         "bit error rates at this point are 1.3 × 10^−2^, 5.9 × 10^−2^ and 1.2 × 10^−1^.")
    figure(e, os.path.join(ASSETS, "constellations.png"),
           "Received constellations at E~b~/N~0~ = 4 dB. The 64-QAM cloud spans several decision "
           "regions, while QPSK remains separable.", width=455)
    p(e, "This is the clearest illustration of why link adaptation exists. A receiver facing the "
         "right-hand panel would not deliver six bits per symbol; it would deliver a stream of "
         "errors and trigger retransmissions. The same channel, used with QPSK, would deliver two "
         "bits per symbol at an error rate two orders of magnitude lower. The scheduler's "
         "decision to step down is therefore not a conservative choice but a calculation of "
         "throughput after retransmission.")

    section(e, "5.3", "Bit Error Rate Results", "c5s3")
    p(e, "The error-rate chart condenses the constellation behaviour into a single curve per "
         "scheme. The markers follow the slider, and the dashed vertical line marks the current "
         "operating point, so the relationship between the visual cloud and the numerical error "
         "rate is immediate.")
    figure(e, os.path.join(ASSETS, "ber.png"),
           "Bit error rate chart and summary panel of the dashboard at E~b~/N~0~ = 10 dB.",
           width=455)
    p(e, "The computed error rates at selected operating points are collected in the table below. "
         "Each value is the analytic bit error rate of the corresponding square constellation at "
         "the stated E~b~/N~0~.", space_after=2)
    table(e,
          ["E~b~/N~0~ (dB)", "QPSK", "16-QAM", "64-QAM"],
          [["0", "7.9 × 10^−2^", "1.4 × 10^−1^", "1.7 × 10^−1^"],
           ["4", "1.3 × 10^−2^", "5.9 × 10^−2^", "1.2 × 10^−1^"],
           ["8", "1.9 × 10^−4^", "9.3 × 10^−3^", "5.2 × 10^−2^"],
           ["12", "9.0 × 10^−9^", "1.4 × 10^−4^", "9.7 × 10^−3^"],
           ["16", "2.3 × 10^−19^", "6.3 × 10^−9^", "2.2 × 10^−4^"]],
          [110, 110, 110, 110],
          caption="Table 2: Bit error rate of the three schemes at selected values of E~b~/N~0~.")
    p(e, "Two observations follow. First, the curves do not cross: at every point on the axis the "
         "denser constellation has the higher error rate, as the geometry of Section 2.2 "
         "requires. Second, the decay rate is steepest for QPSK. Between 8 dB and 12 dB the QPSK "
         "error rate falls by four and a half decades, while 64-QAM falls by less than one. The "
         "difference in slope is why the horizontal separation between the curves narrows at very "
         "low error rates and why the ordering of the schemes is never ambiguous in the operating "
         "range of a real link.")

    section(e, "5.4", "Spectral Efficiency and Required E~b~/N~0~", "c5s4")
    p(e, "The summary panel of the dashboard inverts the error-rate curve. For each scheme it "
         "reports the E~b~/N~0~ at which the bit error rate reaches 10^−3^, and expresses the "
         "result as a margin above the QPSK baseline. The values are 6.8 dB for QPSK, 10.5 dB for "
         "16-QAM and 14.8 dB for 64-QAM, that is, margins of +3.7 dB and +8.0 dB.")
    table(e,
          ["Scheme", "Bits/symbol", "E~s~/N~0~ offset", "E~b~/N~0~ at 10^−2^", "at 10^−3^", "at 10^−4^"],
          [["QPSK", "2", "+3.0 dB", "4.3 dB", "6.8 dB", "8.4 dB"],
           ["16-QAM", "4", "+6.0 dB", "7.9 dB", "10.5 dB", "12.2 dB"],
           ["64-QAM", "6", "+7.8 dB", "12.0 dB", "14.8 dB", "16.5 dB"]],
          [72, 78, 92, 92, 74, 74],
          caption="Table 3: Required E~b~/N~0~ for three target bit error rates.")
    figure(e, os.path.join(FIG, "fig_efficiency.png"),
           "Spectral efficiency of the three schemes and the E~b~/N~0~ required at each target "
           "bit error rate.", width=440)
    p(e, "The trade-off is now explicit. 64-QAM carries three times as many bits per symbol as "
         "QPSK and needs 8 dB more link margin to do so, which is a little under one decibel per "
         "extra bit per symbol. In a link budget, 8 dB corresponds to a factor of 6.3 in "
         "transmitted power, or to a reduction of roughly 40 percent in the radius of the cell "
         "over which the scheme can be sustained with the same antenna configuration.")
    p(e, "This is the quantitative justification for placing the denser constellations in the "
         "inner part of the cell. The scheduler does not choose 64-QAM because it is faster; it "
         "chooses it because, for users whose channel can support it, the extra bits are free at "
         "the margin they already have. For users below the threshold, the same choice would "
         "reduce the delivered throughput.")

    section(e, "5.5", "Error Vector Magnitude", "c5s5")
    p(e, "The error vector magnitude expresses the same noise in the amplitude domain. It is "
         "defined as the root-mean-square distance between the received symbol and the ideal "
         "point, normalised to the root-mean-square symbol amplitude. For a unit-energy "
         "constellation with per-dimension noise variance N~0~/2 the expected value is:")
    formula(e, "EVM = √(N~0~/E~s~) × 100 %  =  100 / √(E~s~/N~0~)")
    figure(e, os.path.join(FIG, "fig_evm.png"),
           "Error vector magnitude against E~s~/N~0~, with the operating points at which each "
           "scheme reaches a bit error rate of 10^−3^ marked.", width=400)
    p(e, "The figure is instructive because it shows the three schemes at the same error rate "
         "rather than at the same signal-to-noise ratio. QPSK reaches 10^−3^ at 9.8 dB of "
         "E~s~/N~0~, where the EVM is still about 32 percent; 16-QAM needs 16.5 dB and an EVM of "
         "14.9 percent; 64-QAM needs 22.6 dB and an EVM of 7.5 percent. The denser constellation "
         "tolerates a smaller fractional error for the same bit error rate, which is precisely "
         "the statement that its decision regions are smaller.")
    p(e, "EVM is the quantity a laboratory instrument reports, and it is the quantity a hardware "
         "engineer budgets for. Translating the curves into EVM therefore connects the analysis "
         "of this report to the measurement side: a transmitter specified for 8 percent EVM at "
         "the antenna is adequate for 64-QAM at 10^−3^ and comfortable for 16-QAM, while a "
         "transmitter that drifts to 20 percent EVM will fail the 16-QAM requirement and be "
         "restricted to QPSK.")

    section(e, "5.6", "Discussion", "c5s6")
    p(e, "Three results of the study are worth stating explicitly. The first is that the penalty "
         "for spectral efficiency is close to three decibels per bit in E~s~/N~0~ terms. The "
         "figure follows from the geometry of the constellation and is not an artefact of the "
         "particular approximation used; it is the reason link adaptation steps through the "
         "scheme table in roughly three-decibel increments.")
    p(e, "The second is that the ordering of the schemes is stable. No crossing of the curves "
         "occurs anywhere in the range 0 to 20 dB, so a receiver that can decode QPSK can always "
         "fall back to it, and a scheme that fails at a given margin will always fail at a lower "
         "one. This monotonicity is what makes a threshold-based scheduler safe.")
    p(e, "The third concerns the interpretation of the constellation plots. The visual impression "
         "of a cloud is not merely illustrative: its radius is the standard deviation of the "
         "noise, and the ratio of that radius to the cell spacing is the quantity that appears in "
         "the argument of the Q-function. The dashboard therefore displays the same number twice, "
         "once as a picture and once as a logarithm, and the two agree by construction.")
    p(e, "The limitations of the study should also be stated. The channel is AWGN only: there is "
         "no fading, no multipath, no phase noise and no nonlinearity, and the error probability "
         "is analytic rather than simulated. These simplifications are appropriate for isolating "
         "the effect of the constellation, but they make the reported E~b~/N~0~ values "
         "optimistic. A real link adds an implementation margin of several decibels for each "
         "impairment, and a coded link operates at a lower signal-to-noise ratio than the uncoded "
         "curves suggest because the code trades bandwidth for power.")


def ch6(e):
    chapter(e, "Chapter-6")
    section(e, "6.1", "Conclusion", "c6s1")
    p(e, "The link performance of QPSK, 16-QAM and 64-QAM over an AWGN channel has been analysed "
         "on a common basis, with unit average symbol energy, Gray-coded square constellations "
         "and a single noise model. The study confirms the expected relationship between "
         "constellation size, spectral efficiency and noise sensitivity, and quantifies it: 2, 4 "
         "and 6 bits per symbol at E~b~/N~0~ requirements of 6.8, 10.5 and 14.8 dB for a bit "
         "error rate of 10^−3^.")
    p(e, "The constellation diagrams make the mechanism visible. At 4 dB the 64-QAM cloud spans "
         "several decision regions while QPSK remains separable, and at 10 dB all three are "
         "usable but with very different margins. The error-rate curves make the same statement "
         "numerically, falling by an order of magnitude for roughly every 1.6 dB of additional "
         "signal-to-noise ratio at the operating point.")
    p(e, "The trade-off is therefore not a matter of preference but of arithmetic. Each "
         "additional bit per symbol costs close to three decibels of symbol-to-noise ratio, and "
         "the choice of scheme is the choice of how much of the available margin to spend on "
         "throughput. Adaptive modulation and coding in LTE and 5G is the mechanism that makes "
         "this choice per user and per subframe, and the thresholds it uses are precisely the "
         "values computed here.")
    p(e, "The interactive implementation adds a practical dimension to the analysis. Because the "
         "tool recomputes every quantity from the same equations, it can be used to explore the "
         "operating range, to check a link-budget calculation, or to demonstrate in a classroom "
         "why a denser constellation is not automatically a better one.")

    section(e, "6.2", "Future Scope", "c6s2")
    p(e, "Several extensions follow naturally from this work:", space_after=3)
    bullets(e, [
        "**Fading channels.** Replacing the AWGN channel with Rayleigh or Rician fading would "
        "introduce the diversity and coding gains that dominate real cellular links, and would "
        "require averaging the error probability over the fading distribution.",
        "**Coded modulation.** Adding convolutional, turbo or LDPC coding would allow the coded "
        "curves to be compared with the uncoded ones, and would show the coding gain that closes "
        "part of the gap to the Shannon bound.",
        "**Multicarrier operation.** Combining the mapper with OFDM would reproduce the subcarrier "
        "structure of LTE and NR, and would make it possible to study the effect of frequency-"
        "selective channels and of a per-subcarrier modulation choice.",
        "**Hardware impairments.** Phase noise, IQ imbalance and amplifier nonlinearity could be "
        "added to the model, and the resulting EVM could be compared with the laboratory "
        "specification of a transmitter.",
        "**Measured data.** The analytic curves could be validated against captured symbols from "
        "a software-defined radio, closing the loop between simulation and measurement.",
    ])
    p(e, "Each of these extensions preserves the structure of the present tool: a constellation "
         "model, a channel model and a decision rule, so a new channel or scheme can be added "
         "without changing the interface.")

    section(e, "6.3", "References", "c6s3")
    refs = [
        "T. S. Rappaport, *Wireless Communications: Principles and Practice*, 2nd ed. Upper "
        "Saddle River, NJ: Prentice Hall, 2002.",
        "J. G. Proakis and M. Salehi, *Digital Communications*, 5th ed. New York: McGraw-Hill, "
        "2008.",
        "S. Haykin, *Communication Systems*, 4th ed. New York: John Wiley & Sons, 2001.",
        "A. Goldsmith, *Wireless Communications*. Cambridge: Cambridge University Press, 2005.",
        "C. E. Shannon, “A mathematical theory of communication,” *Bell System Technical "
        "Journal*, vol. 27, no. 3, pp. 379–423, Jul. 1948.",
        "3GPP, “NR; Physical channels and modulation,” **3GPP TS 38.211**, Release 17, 2022.",
        "3GPP, “NR; Physical layer procedures for data,” **3GPP TS 38.214**, Release 17, 2022.",
        "J. G. Andrews *et al.*, “What will 5G be?,” *IEEE Journal on Selected Areas in "
        "Communications*, vol. 32, no. 6, pp. 1065–1082, Jun. 2014.",
        "W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, *Numerical Recipes "
        "in C*, 2nd ed. Cambridge: Cambridge University Press, 1992.",
        "M. K. Simon and M.-S. Alouini, *Digital Communication over Fading Channels*, 2nd ed. "
        "New York: John Wiley & Sons, 2005.",
    ]
    for i, r in enumerate(refs, 1):
        e.para(f"{i}.  {r}", indent_first=0, indent_rest=20, space_after=1.5,
               align="left")


def annexure(e):
    e.new_page()
    ANCHORS["annex"] = e.page_no
    e.text_at(LEFT, TOP, "**Annexure:-**", 16.86, 1)
    e.y = 110
    p(e, "The following listing contains the core of the analysis: the mathematics, the "
         "constellation builder and the error-rate computation. The interface code and the "
         "canvas drawing routines are omitted for brevity; the complete source is a single HTML "
         "file of about nine hundred lines.")
    code = r"""/* ---------- Gaussian tail ---------- */
function erfc(x){
  const z = Math.abs(x), t = 1 / (1 + z / 2);
  const r = t * Math.exp(-z*z - 1.26551223 +
      t*(1.00002368 + t*(0.37409196 + t*(0.09678418 +
      t*(-0.18628806 + t*(0.27886807 + t*(-1.13520398 +
      t*(1.48851587 + t*(-0.82215223 + t*0.17087277)))))))));
  return x >= 0 ? r : 2 - r;
}
const qfunc = x => 0.5 * erfc(x / Math.SQRT2);

/* ---------- analytic BER of square QAM ---------- */
function berOf(k, M, ebn0db){
  const ebn0 = Math.pow(10, ebn0db / 10);
  const arg  = Math.sqrt(3 * k / (M - 1) * ebn0);
  return (4 / k) * (1 - 1 / Math.sqrt(M)) * qfunc(arg);
}

/* ---------- inverse: Eb/N0 for a target BER ---------- */
function requiredEbn0(k, M, target){
  let lo = -10, hi = 40;
  for (let i = 0; i < 60; i++){
    const mid = (lo + hi) / 2;
    if (berOf(k, M, mid) > target) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

/* ---------- unit-energy square constellation ---------- */
function buildConstellation(M){
  const side = Math.sqrt(M);
  const norm = Math.sqrt(2 * (M - 1) / 3);
  const pts = [];
  for (let i = 0; i < side; i++)
    for (let j = 0; j < side; j++)
      pts.push([(2*i - (side-1)) / norm, (2*j - (side-1)) / norm]);
  return pts;
}

/* ---------- Box-Muller Gaussian sample ---------- */
let cache = null;
function gauss(){
  if (cache !== null){ const v = cache; cache = null; return v; }
  let u, v, s;
  do { u = Math.random()*2 - 1; v = Math.random()*2 - 1;
       s = u*u + v*v; } while (s >= 1 || s === 0);
  const m = Math.sqrt(-2 * Math.log(s) / s);
  cache = v * m;
  return u * m;
}

/* ---------- received symbols at a given Eb/N0 ---------- */
function receive(points, k, ebn0){
  const esn0  = Math.pow(10, (ebn0 + 10 * Math.log10(k)) / 10);
  const sigma = 1 / Math.sqrt(2 * esn0);
  return points.map(p => [p[0] + gauss() * sigma,
                          p[1] + gauss() * sigma]);
}

/* ---------- scheme table ---------- */
const SCHEMES = [
  { name:'QPSK',   M:4,  k:2, color:'#2E6BF6' },
  { name:'16-QAM', M:16, k:4, color:'#00A88A' },
  { name:'64-QAM', M:64, k:6, color:'#F2536D' }
];
SCHEMES.forEach(s => s.points = buildConstellation(s.M));

/* ---------- readouts ---------------------------------------------- */
const ebn0 = parseFloat(slider.value);
SCHEMES.forEach(sch => {
  const esn0 = ebn0 + 10 * Math.log10(sch.k);
  sch.esEl.textContent  = esn0.toFixed(1) + ' dB';
  sch.berEl.textContent = sci(berOf(sch.k, sch.M, ebn0));
});"""
    for line in code.split("\n"):
        e.raw(line.replace("\t", "    "), size=9.3, leading=12.3, x0=LEFT + 6)


# --------------------------------------------------------------------- build
def build(path, name, roll, anchors=None, prev_figs=None):
    global ANCHORS, FIGPAGES, FIGN, FIGCAPS
    ANCHORS, FIGPAGES, FIGN = dict(anchors or {}), {}, [0]
    FIGCAPS = []
    e = Engine()
    title_page(e, name, roll)
    certificate(e, name, roll)
    declaration(e, name, roll)
    ANCHORS["ack"] = e.page_no + 1
    acknowledgements(e)
    abstract(e)
    contents(e, prev_figs)
    ch1(e)
    ch2(e)
    ch3(e)
    ch4(e)
    ch5(e)
    ch6(e)
    annexure(e)
    e.save(path)
    return dict(ANCHORS), dict(FIGPAGES), list(FIGCAPS)


def main():
    public = "--public" in sys.argv
    name = os.environ.get("REPORT_AUTHOR", "[Student Name]")
    roll = os.environ.get("REPORT_ROLL", "[Roll Number]")
    if public:
        name, roll = "[Student Name]", "[Roll Number]"
    out = os.path.join(ROOT, "CellularAnalysis" + ("_public" if public else "") + ".pdf")
    anchors, figs = None, []
    for _ in range(4):
        new_anchors, _, new_figs = build(out, name, roll, anchors, figs)
        if new_anchors == anchors and new_figs == figs:
            break
        anchors, figs = new_anchors, new_figs
    print("wrote", out, "pages:", __import__("pymupdf").open(out).page_count)


if __name__ == "__main__":
    main()
