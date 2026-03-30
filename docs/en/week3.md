# Week 3: Advanced Modeling & Load Testing {#page:w3}

## Week 3 Overview & Objectives {#w3-overview}

Week 3 focuses on bridging the gap between an ideal simulation and real hardware by (1) improving the simulation model (wheel dynamics + ground friction), (2) performing controlled **load tests** on the real system, and (3) systematically tuning and comparing controllers (PID vs. at least one advanced method such as LQR or MPC).\

**Objectives:**

- Extend the simulation to include wheel dynamics and a friction model, and document the assumptions clearly

- Demonstrate stable inversion under added load and record repeatable test evidence

- Tune PID gains in MATLAB under load and compare with at least one alternative controller (e.g., LQR/MPC)

- Compare simulation vs hardware performance using consistent metrics and plots

!!! warning
    - **Secure the load firmly.** If the load falls off, it can damage the hardware or injure people.
    
    - **Avoid prolonged high-frequency rattling.** If you hear harsh buzzing/rattling or see violent vibration, **turn off the battery immediately** (risk of overheating or loosening screws).
    
    - **Start from conservative gains.** Add load increases required torque and makes saturation/tripping more likely.
    
    - **Work on a clear floor and keep hands away from moving wheels.** Prepare a "catch" posture to prevent hard impacts when the system falls.

## Parallel Tasks {#w3-parallel}

Recommended parallel roles: Student A (hardware load attachment + load testing), Student B (simulation model enhancement), Student C (MATLAB tuning + controller comparison). Roles can be rotated, but keep a single shared test log (same naming and metrics).\

- **Student A:** Task A (load attachment and hardware tests) --- [see Section [5.3](#sec:w3-task-a)](#sec:w3-task-a)

- **Student B:** Task B (extend simulation: wheel dynamics + friction) --- [see Section [5.4](#sec:w3-task-b)](#sec:w3-task-b)

- **Student C:** Task C (PID tuning + advanced controller comparison) --- [see Section [5.5](#sec:w3-task-c)](#sec:w3-task-c)

## Task A: Load Attachment and Hardware Tests (Student A) {#sec:w3-task-a}

This task adds controlled load to the cart/pendulum and evaluates stability and performance on real hardware.

### A1. Choose and attach the load

- **Load candidates**: coins/metal washers/small weights or a small object with known mass.

- **Suggested range**: start small (e.g., 50--100 g total) and increase gradually only if stable.

- **Where to attach**: record the attachment location (height and forward/back offset). A higher or more offset load changes the dynamics more strongly.

- **Attachment method**: use tape/zip-tie/rubber bands such that the load cannot slide or detach during vibration.

### A2. Hardware test protocol (baseline $\rightarrow$ load)

1.  **Baseline run (no load)**: run your best Week 2 configuration and record a short video.

2.  **Loaded run**: attach the load and repeat the same test conditions (same floor, similar initial angle, same gains).

3.  **Controller variations**: for each load condition, test at least:\
    (i) tuned PID (or PD) and (ii) one alternative controller configuration (from Task C).

4.  **Stop criteria**: if the motor driver trips repeatedly, if the system rattles violently, or if temperature rises noticeably, stop and reduce aggressiveness.

### A3. What to record (minimum evidence)

- A clear video showing the system balancing under load (include a few seconds before/after enabling control)

- A simple test log table with: load mass, attachment location, gains/controller type, sampling rate (if changed), notes (success/failure)

- If available, screenshots/plots of key signals (angle, control input, encoder-based motion) for at least one baseline and one loaded trial

## Task B: Extend Simulation (Wheel Dynamics + Ground Friction) (Student B) {#sec:w3-task-b}

This task improves the simulation so it can explain observed differences between Week 2 simulation and hardware.

### B1. Add wheel dynamics

- Include wheel inertia and motor-to-wheel dynamics consistently (at minimum: additional rotational inertia term and its coupling to $x$)

- Ensure the output signals needed for comparison are available (e.g., $\theta$, $x$, control input, and any estimated velocities)

### B2. Add a friction model

- Implement at least one friction effect such as:\
  **viscous friction** ($F=-b\dot{x}$) and/or **Coulomb friction** ($F=-F_c\,\mathrm{sgn}(\dot{x})$), or an equivalent block in Simulink

- Document assumptions: which friction terms are used, parameter values, and how you selected/estimated them

### B3. Run and document enhanced simulation

- Compare Week 2 (simplified) vs Week 3 (enhanced) simulation for the same controller settings

- Provide at least: time responses of $\theta$ and $x$ (or their proxies), and control input (check saturation)

- Save plots in a consistent format so they can be included in the Week 3 group report

## Task C: PID Tuning and Controller Comparison (Student C) {#sec:w3-task-c}

This task tunes PID gains in MATLAB under load and compares with at least one alternative controller.

### C1. Tune PID (or PD) under load in MATLAB

- Use your Week 3 enhanced model (including load) for tuning; if you use PID Tuner, save the tuned gains and the tuning settings. If you tune directly from a Simulink/Simscape model, you typically need **Simulink Control Design** (for model linearization). If you tune using an LTI plant model (transfer function/state-space), **Control System Toolbox** is typically sufficient.

- Record the final gains and the expected step/disturbance response (rise time, overshoot, settling time)

- Ensure the control input remains within realistic limits (avoid persistent saturation in simulation)

### C2. Try at least one advanced controller (recommended: LQR)

- **LQR (recommended)**: linearize your model, choose $Q,R$, compute gains, and simulate under baseline and load. If you linearize from the Simulink/Simscape model, **Simulink Control Design** is typically required; alternatively, you can use the linearized $A,B$ matrices derived in Section 2 (then **Control System Toolbox** is sufficient for `lqr`).

- **MPC (optional)**: if attempted, clearly state constraints, horizon, and sampling time

- Compare against PID using the same test scenario and metrics

### C3. Simulation vs hardware comparison

- Define common metrics (pick at least three): stability duration, peak angle, RMS angle, position drift, control effort (RMS or peak), saturation time ratio

- Summarize results in a small table for: baseline vs load, PID vs alternative controller, simulation vs hardware

- Briefly explain the gaps (likely causes: friction mismatch, saturation, sensor noise, discretization, delays)

## Week 3 Submission

!!! note "Submission"
    Your work should show a clear progression: **enhanced model** $\rightarrow$ **tuned control** $\rightarrow$ **validated under load on real hardware**. Submit a **single group report** containing:
    
      --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      **Deliverable**                **Max**  **Scoring guide**
      ----------------------------- --------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      Enhanced simulation results       6     **6 pts:** model includes wheel inertia + ground friction + numerical parameter values, all documented.\
                                              **4 pts:** two of the three elements included.\
                                              **2 pts:** one of the three elements included.\
                                              **0 pts:** no enhancement over Week 2 model.
    
      Load test video                   7     **7 pts:** stable inversion $\geq$5 s under load; load mass and attachment location clearly identified (caption/overlay).\
                                              **5 pts:** stable under load but load mass/location not quantified.\
                                              **2 pts:** load test attempted with documentation but stability not achieved.\
                                              **0 pts:** not submitted.
    
      Controller comparison             7     **7 pts:** PID metrics reported (rise time, overshoot, settling time) *and* a structurally different controller (LQR / state feedback / feedforward) compared using the same metrics.\
                                              **4 pts:** PID only, or alternative from the same family (e.g., PID variant).\
                                              **2 pts:** qualitative discussion only (no quantitative metrics).
      --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

