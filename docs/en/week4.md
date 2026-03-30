# Week 4: Final Presentation

## Week 4 Overview & Objectives

Week 4 is the final wrap-up. You will present your design and results, demonstrate a working system, and answer technical questions. The key is to provide a coherent evidence chain:\
**modeling assumptions** $\rightarrow$ **controller design** $\rightarrow$ **implementation** $\rightarrow$ **validation (simulation and hardware)** $\rightarrow$ **lessons learned**.\

**Objectives:**

- Prepare a clear 10-minute presentation (slides) explaining theory, design choices, and results

- Demonstrate stable inverted-pendulum control on hardware (live)

- Answer questions with evidence (plots, logs, reasoning, and limitations)

## Week 4 Requirements

- **Presentation)**: 10 minutes, 8--12 slides, with a clear story from modeling assumptions to controller design, implementation, and validation (simulation + hardware).

- **Live demo**: demonstrate stable inverted-pendulum control on hardware with a safe, repeatable setup (have a conservative fallback configuration ready).

- **Evidence for Q&A**: be able to justify design choices using plots/logs/metrics; explain simulation--hardware gaps, limits, and robustness under load/disturbances.

## Week 4 Submission

!!! note "Submission"
    Submit the following package and deliver a live presentation:
    
      --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      **Deliverable**       **Max**  **Scoring guide**
      -------------------- --------- -------------------------------------------------------------------------------------------------------------------------------------------------
      Slides (PDF)            10     **10 pts:** all four elements covered with supporting data: (1) theory, (2) design, (3) validation (sim + hardware), (4) lessons learned.\
                                     **7 pts:** three of the four elements covered.\
                                     **3 pts:** $\leq$2 elements, or text-only slides without data.
    
      Final demo video        10     **10 pts:** stable run $\geq$10 s with clear enable/disable sequence (a few seconds shown before and after enabling control).\
                                     **6 pts:** stable run but enable/disable sequence unclear or missing.\
                                     **2 pts:** demo fails but failure is honestly documented.\
                                     **0 pts:** not submitted.
    
      Presentation & Q&A      10     **5 pts:** $\geq$2 technical questions answered correctly during Q&A.\
                                     **5 pts:** answers are consistent with the submitted materials (slides, video, report).\
                                     Partial credit applied within each sub-criterion.
      --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[^1]: Course materials repository: <https://github.com/UTokyo2026/UTokyo-Control-Practice-2026>

[^2]: The proportionality coefficient between back EMF and speed is called \"back EMF constant,\" but when units are unified to the SI system, the back EMF constant and torque constant become the same value. This can be confirmed by calculating considering energy conservation.

[^3]: Appendix [\[app:circuit\]](#app:circuit): Circuit example.

[^4]: Appendix [\[app:drv8832\]](#app:drv8832): DRV8832 datasheet (Texas Instruments).

[^5]: Appendix [\[app:tpr105f\]](#app:tpr105f): TPR-105F datasheet.

[^6]: Appendix [\[app:ld1117v33\]](#app:ld1117v33): LD1117V33 datasheet.

[^7]: A video demonstration of the mechanical assembly process is available in the course materials repository:

[^8]: For a complete parts list with detailed specifications and quantities, see Appendix [\[app:partslist\]](#app:partslist).

[^9]: Appendix [\[app:re280ra\]](#app:re280ra): RE-280RA datasheet (Mabuchi Motor).

[^10]: There are various other microcontroller series such as Arduino, Raspberry PI, PIC, etc.

[^11]: Keil Studio Cloud: <https://studio.keil.arm.com/>

[^12]: Access the course materials repository at <https://github.com/UTokyo2026/UTokyo-Control-Practice-2026>

[^13]: Processing is a free, open-source software for visual programming. You can download it from <https://processing.org/>. As of 2026, the currently available major release is Processing 4. For more instructions, see Appendix [\[app:processing\]](#app:processing).

[^14]: Fritzing installers (shared Google Drive): <https://drive.google.com/drive/folders/1CwJ8srD090W6hOeP39BXLUZOVy883Kn2?usp=sharing>

[^15]: Appendix [\[app:circuit\]](#app:circuit): Circuit example.

[^16]: A video demonstration of the circuit assembly process is available in the course materials repository:

[^17]: Appendix [\[app:circuit\]](#app:circuit): Circuit example.

[^18]: Appendix [\[app:circuit\]](#app:circuit): Circuit example.

[^19]: Appendix [\[app:circuit\]](#app:circuit): Circuit example.

[^20]: This time we use a reflective photo-interrupter so it is a black and white pattern, but generally transmissive photo-interrupters and slit disks are often used

[^21]: Access the course materials repository at <https://github.com/UTokyo2026/UTokyo-Control-Practice-2026>

[^22]: Appendix [\[app:processing\]](#app:processing): Processing Oscilloscope Manual.

[^23]: A video demonstration of the debugging and tuning process is available in the course materials repository:

[^24]: If using Matlab, freqz(b,a) or bode(tf(b,a,sampling time)) allows checking the frequency response of the filter.

[^25]: In a 1st order LPF, phase delays by 90 degrees in high frequency band. Considering the case where inclination angle changes sinusoidally, its derivative (= angular velocity) must be advanced by 90 degrees phase relative to inclination angle, but at high frequencies, phase delays by 90 degrees due to the filter, so passing the differentiation result through the filter results in the same phase as the original inclination angle. This is no longer differentiation. Therefore, at high frequencies, even if intending to do derivative control, it is actually the same as doing proportional control. Thus, easily increasing derivative gain makes proportional gain substantially large in high frequency band, resulting in oscillatory and unstable response.\
    By the way, if it is a 2nd order filter, phase delays up to 180 degrees, but 180 degree phase delay is the same as inverting the signal. Therefore, multiplying a signal delayed by 180 degrees by derivative gain results in movement exactly opposite to original D control (= damper) (increasing velocity).

[^26]: Ratio of P gain and D gain is easy to understand when compared with standard form of 2nd order lag. If spring constant and damping coefficient are $K_p$ and $K_d$, transfer function from external force to position is $$\begin{equation}
    \frac{X(s)}{F(s)}=\frac{1}{ms^2+K_d s+K_p}=\frac{1/m}{s^2+(K_d/m)s+K_p/m} \nonumber
    \end{equation}$$ On the other hand, standard form is $$\begin{equation}
    G(s)=\frac{\omega_n^2}{s^2+2\zeta \omega_n s+\omega_n^2} \nonumber
    \end{equation}$$ Comparing both, it can be seen that $K_d/K_p = 2\zeta/\omega_n$. For example, if damping ratio $\zeta=0.5$ (degree of slight overshoot), ratio of D gain and P gain is natural angular frequency $\omega_n$. In first pendulum angle control, natural vibration was several Hz, so angular frequency should have been about 20rad/s, but in position control natural vibration is 0.1Hz range, so angular frequency is about 1rad/s. Therefore, P gain and D gain become same order.

[^27]: <https://www.tij.co.jp/product/jp/DRV8832#tech-docs>
