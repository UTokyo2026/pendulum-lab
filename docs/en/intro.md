!!! warning
# Class Calendar

Sessions: **Mondays, 13:00--18:30 (JST, Asia/Tokyo)**; The course runs in **three cohorts** (**4 weeks** each). **Week 0** marks preparation; please complete required setup *before* Week 1 begins (Week 0 is not shown).

**Legend:** ; ; ; ; **Badge:** `C#-W#` = cohort/week, `OFF` = no class.

**Apr 2026**

**May 2026**

**Jun 2026**

**Jul 2026**

# Course Schedule and Weekly Tasks

\|c\|L4.5cm\|L7cm\|L3.5cm\| **Week** & **Tasks** & **Individual Responsibilities** & **Submissions**\
**Week 0** & **Preparation & Course Study**\
- Study lecture notes and theory\
- Prepare computer and software environment\
- Install required software / set up accounts (MATLAB, Keil Studio Cloud, Processing, Fritzing) & **All students:**\
- Read through the entire lecture text\
- Prepare your PC environment

**Student A:** check the hardware kit contents ([see Appendix [\[app:partslist\]](#app:partslist)](#app:partslist))\
**Student B:** set up Keil Studio Cloud account + install Processing ([see Section [3.3.2](#sec:w1-microcontroller-setup)](#sec:w1-microcontroller-setup); [see Appendix [\[app:processing\]](#app:processing)](#app:processing))\
**Student C:** install Fritzing + MATLAB ([see Section [3.3.3](#sec:w1-breadboard-wiring-design)](#sec:w1-breadboard-wiring-design); [see Section [4.5.2](#sec:matlab-setup)](#sec:matlab-setup)) & None\
**Week 1** & **Assembly & Bring-up**\
- Mechanical assembly\
- Microcontroller bring-up and debugging\
- Breadboard circuit design (Fritzing)\
- Integration and debugging & **Step 1 (individual):**\
- **Student A:** mechanical assembly ([see Section [3.3.1](#sec:w1-mechanical-assembly)](#sec:w1-mechanical-assembly))\
- **Student B:** microcontroller bring-up/debug ([see Section [3.3.2](#sec:w1-microcontroller-setup)](#sec:w1-microcontroller-setup))\
- **Student C:** Fritzing breadboard design ([see Section [3.3.3](#sec:w1-breadboard-wiring-design)](#sec:w1-breadboard-wiring-design))\
**Step 2 (team):** integrate and debug successfully ([see Section [3.4](#sec:w1-circuit-assembly)](#sec:w1-circuit-assembly)) & - Stand demo video\
**Week 2** & **Encoder & Position Control**\
- Build encoder + validate signals\
- Close the loop: position control (compare with simulation) & **Student A:** encoder hardware ([see Section [4.3](#sec:w2-task-a)](#sec:w2-task-a))\
**Student B:** encoder readout + control on mbed ([see Section [4.4](#sec:w2-task-b)](#sec:w2-task-b))\
**Student C:** simulation + comparison ([see Section [4.5](#sec:w2-task-c)](#sec:w2-task-c)) & **Group report:**\
- Position-control video\
- Encoder A/B plots\
- Sim vs. hardware comparison\
**Week 3** & **Advanced Modeling & Load Testing**\
- Add wheel dynamics and ground friction to simulation\
- Add load to the cart/pendulum and test on hardware\
- Tune PID gains in MATLAB and try other controllers (LQR/MPC, etc.) and compare performance & **Student A:**\
- Attach load (e.g., weights) to the inverted pendulum cart\
- Run hardware tests under load, record video\
**Student B:**\
- Extend the MATLAB/Simscape model: wheel dynamics + ground friction\
- Run and document the enhanced simulation\
**Student C:**\
- Tune PID gains in MATLAB with added load (e.g., PID Tuner; for Simulink-model-based tuning, Simulink Control Design is needed)\
- Then try other controllers (LQR, MPC, etc.) and compare simulation vs real results & **Group report:**\
- Enhanced simulation results\
- Load test video\
- PID tuning + controller comparison documentation\
**Week 4** & **Final Presentation**\
- Prepare presentation slides\
- Demonstrate working system\
- Q&A and discussion & **All students:**\
- Prepare 10-minute presentation covering: theory, design, simulation, hardware results, challenges\
- Demonstrate live inverted pendulum control\
- Answer technical questions & **Final submission:**\
- Slides\
- Final demo video\
- Presentation & Q&A\

[]

# Grading Criteria

\|C1.35cm\|L3.0cm\|L3.3cm\|L7.4cm\| **Week** & **Deliverables** & **Criterion** & **Score tiers**\

**W0**\
(0 pts)

& Preparation check & Completion only & No submission required.\
& & Standing (max 20) & **20** --- upright $\geq$15 s, full system in frame\
**12** --- achieved but $<$15 s or marginal\
**0** --- not achieved\
& & Safety & assembly (max 5) & **5** --- full assembly visible\
**0** --- not visible\
& & Video clarity (max 5) & **5** --- all key parts unobscured throughout\
**3** --- key behavior still identifiable\
**0** --- unusable\
& & Position control (max 8) & **8** --- inversion $\geq$10 s within $\pm$0.5 m of set-point\
**5** --- inversion held but position drift large\
**0** --- inversion lost within 5 s\
& & Encoder (max 7) & **7** --- A/B waveforms labeled *and* direction reversal verified\
**5** --- waveforms shown, direction not verified\
**2** --- pulse count only, no phase analysis\
**0** --- not submitted\
& & Simulation (max 5) & **5** --- $x(t)$, $\dot{x}(t)$ plots sim vs. hardware *and* discrepancy explained\
**3** --- plots included, no explanation\
**1** --- qualitative description only\
& & Enhanced model (max 6) & **6** --- wheel inertia + friction + numerical params\
**4** --- two of three elements\
**2** --- one of three elements\
**0** --- no enhancement over W2\
& & Load test (max 7) & **7** --- stable $\geq$5 s *and* load mass/location identified\
**5** --- stable but load unquantified\
**2** --- attempted with documentation\
**0** --- not submitted\
& & Controller comparison (max 7) & **7** --- PID metrics (rise time, overshoot, settling) + structurally different controller (LQR / state feedback / feedforward) with same metrics\
**4** --- PID only, or same-family alternative\
**2** --- qualitative discussion only\
& & Slides (max 10) & **10** --- all four elements with data: theory, design, validation, lessons\
**7** --- three of four elements\
**3** --- $\leq$2 elements or text-only\
& & Demo video (max 10) & **10** --- stable $\geq$10 s *and* enable/disable sequence clear\
**6** --- stable but enable/disable sequence unclear\
**2** --- demo fails but honestly documented\
**0** --- not submitted\
& & Q&A (max 10) & **5** --- $\geq$2 technical questions answered correctly\
**5** --- answers consistent with submitted materials\
*Partial credit applied within each sub-criterion.*\

# **!!! Please Read Before the Exercise** !!!

- **Pre-study of this text**: Before starting the exercise, read this text to understand the overview of the work and the theoretical background. Starting work without reading the text may lead to fatal mistakes that make it difficult to continue the exercise.

- **Course Materials**: All supplementary materials (debugging tools, example programs, appendix PDFs, MATLAB models) are provided in the folder[^1]. The subfolder contains three essential tools with complete documentation (README files in both Markdown and PDF formats). The tool includes the complete inverted pendulum control program that you will use in Section [\[sec:inverted-experiment\]](#sec:inverted-experiment).

- **PC Preparation**: For this practical exercise, we will use the PCs in the design exercise room, so you do not need to prepare your own PC. However, it is possible to use your own PC. In that case, Windows or Macintosh is required. Also, a USB port (Type-A) is required to connect to the control microcontroller. If you only have a Type-C port, please prepare a hub that can connect to Type-A.

- **Work on the day**: Installation of the programming environment and assembly of the mechanism will be explained on the day of the exercise.

[^1]: Course materials repository: <https://github.com/UTokyo2026/UTokyo-Control-Practice-2026>
