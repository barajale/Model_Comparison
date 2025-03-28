
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import ConnectionPatch


def plot_vabc_grid(pf_df, sim_df,
                   t1_start=11.4, t1_end=11.6,
                   t2_start=11.9, t2_end=12.3,
                   f_time1=None, f_time2=None):
    """
    Plots Vabc for Simulink and PowerFactory in a 4x2 layout:
    Row 1: Simulink full span
    Row 2: Simulink zoomed start | end
    Row 3: PowerFactory zoomed start | end
    Row 4: PowerFactory full span
    """
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}
    line_style2 = {'color': 'black', 'linestyle': '-', 'linewidth': 0.8}
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle("Vabc", fontsize=16)
    
    # --- Add horizontal divider line ---
    # --- Add horizontal divider between Simulink and PowerFactory ---
    fig.add_artist(plt.Line2D([0, 1], [0.475, 0.475], color='black', linewidth=1.0, linestyle='-'))




    # Create 4x2 grid layout
    gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1])

    # === Simulink Full (Row 1) ===
    sim_full_ish = sim_df[(sim_df['time'] >= 10.0) & (sim_df['time'] <= 13.5)]
    
    ax_sim_full = fig.add_subplot(gs[0, :])
    ax_sim_full.plot(sim_full_ish['time'], sim_full_ish['v_a'], label='Va', color='tab:blue', zorder=0)
    ax_sim_full.plot(sim_full_ish['time'], sim_full_ish['v_b'], label='Vb', color='tab:green', zorder=0)
    ax_sim_full.plot(sim_full_ish['time'], sim_full_ish['v_c'], label='Vc', color='tab:orange', zorder=0)
    ax_sim_full.set_ylabel('Voltage pu')
    #ax_sim_full.set_title("Simulink Full")
    ax_sim_full.grid(True)
    ax_sim_full.legend(loc='upper right')
    if f_time1: ax_sim_full.axvline(f_time1, **line_style)
    if f_time2: ax_sim_full.axvline(f_time2, **line_style)
    if t1_start: ax_sim_full.axvline(t1_start, **line_style2)
    if t1_end: ax_sim_full.axvline(t1_end, **line_style2)
    if t2_start: ax_sim_full.axvline(t2_start, **line_style2)
    if t2_end: ax_sim_full.axvline(t2_end, **line_style2)
    ax_sim_full.set_xlim([sim_full_ish['time'].iloc[0], sim_full_ish['time'].iloc[-1]])


    # === Simulink Zooms (Row 2) ===
    ax_sim_start = fig.add_subplot(gs[1, 0])
    ax_sim_start.zorder = 5
    ax_sim_end = fig.add_subplot(gs[1, 1])
    ax_sim_end.zorder = 5

    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]

    temp = 0
    for ax, data, f_time in zip([ax_sim_start, ax_sim_end], [sim1, sim2], [f_time1, f_time2]):
        ax.plot(data['time'], data['v_a'], color='tab:blue')
        ax.plot(data['time'], data['v_b'], color='tab:green')
        ax.plot(data['time'], data['v_c'], color='tab:orange')
        if temp == 0:
            ax.set_ylabel('Voltage pu')
            temp += 1
        ax.grid(True)
        if f_time: ax.axvline(f_time, **line_style)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])


    # ax_sim_start.set_title("Zoomed Start (Simulink)")
    # ax_sim_end.set_title("Zoomed End (Simulink)")

    # === PowerFactory Zooms (Row 3) ===
    ax_pf_start = fig.add_subplot(gs[2, 0])
    ax_pf_start.zorder = 5
    ax_pf_end = fig.add_subplot(gs[2, 1])
    ax_pf_end.zorder = 5
    
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]

    temp = 0
    for ax, data, f_time in zip([ax_pf_start, ax_pf_end], [pf1, pf2], [f_time1, f_time2]):
        ax.plot(data['time'], data['v_a'], color='tab:blue')
        ax.plot(data['time'], data['v_b'], color='tab:green')
        ax.plot(data['time'], data['v_c'], color='tab:orange')
        if temp == 0:
            ax.set_ylabel('Voltage pu')
            temp += 1
        ax.grid(True)
        if f_time: ax.axvline(f_time, **line_style)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])

    # ax_pf_start.set_title("Zoomed Start (PowerFactory)")
    # ax_pf_end.set_title("Zoomed End (PowerFactory)")

    # === PowerFactory Full (Row 4) ===
    pf_full_ish = pf_df[(pf_df['time'] >= 10.0) & (pf_df['time'] <= 13.5)]
    ax_pf_full = fig.add_subplot(gs[3, :])
    ax_pf_full.plot(pf_full_ish['time'], pf_full_ish['v_a'], label='Va', color='tab:blue', zorder=0)
    ax_pf_full.plot(pf_full_ish['time'], pf_full_ish['v_b'], label='Vb', color='tab:green', zorder=0)
    ax_pf_full.plot(pf_full_ish['time'], pf_full_ish['v_c'], label='Vc', color='tab:orange', zorder=0)
    ax_pf_full.set_ylabel('Voltage pu')
    ax_pf_full.set_xlabel('Time [s]')
    #ax_pf_full.set_title("PowerFactory Full")
    ax_pf_full.grid(True)
    ax_pf_full.legend(loc='upper right')
    if f_time1: ax_pf_full.axvline(f_time1, **line_style)
    if f_time2: ax_pf_full.axvline(f_time2, **line_style)
    if t1_start: ax_pf_full.axvline(t1_start, **line_style2)
    if t1_end: ax_pf_full.axvline(t1_end, **line_style2)
    if t2_start: ax_pf_full.axvline(t2_start, **line_style2)
    if t2_end: ax_pf_full.axvline(t2_end, **line_style2)
    ax_pf_full.set_xlim([pf_full_ish['time'].iloc[0], pf_full_ish['time'].iloc[-1]])
    
    

    # === Connect Zooms to Full using 4-corner ConnectionPatch ===
    for ax_zoom, data, full_ax in [
        (ax_sim_start, sim1, ax_sim_full),
        (ax_sim_end, sim2, ax_sim_full),
        (ax_pf_start, pf1, ax_pf_full),
        (ax_pf_end, pf2, ax_pf_full)
    ]:
        # Get y-limits for zoom and full axes
        y_zoom_min, y_zoom_max = ax_zoom.get_ylim()
        y_full_min, y_full_max = full_ax.get_ylim()

        # Get x-limits (start/end of zoom window)
        x_start = data['time'].iloc[0]
        x_end = data['time'].iloc[-1]

        # Corner mappings: (x, y)
        corners_zoom = [(x_start, y_zoom_min), (x_start, y_zoom_max),
                        (x_end, y_zoom_min),   (x_end, y_zoom_max)]
        
        corners_full = [(x_start, y_full_min), (x_start, y_full_max),
                        (x_end, y_full_min),   (x_end, y_full_max)]

        # Draw 4 connection lines (corner to corner)
        for (xA, yA), (xB, yB) in zip(corners_zoom, corners_full):
            con = ConnectionPatch(
                xyA=(xA, yA), coordsA=ax_zoom.transData,
                xyB=(xB, yB), coordsB=full_ax.transData,
                axesA=ax_zoom, axesB=full_ax,
                color='gray', linestyle='--', linewidth=0.8,
                zorder=2  # below zoom plots (zorder=3), above full plots (zorder=1)
            )
            fig.add_artist(con)  # <== draw to the global canvas (not full_ax)

    # Add vertical section labels
    fig.text(0.01, 0.78, 'Simulink', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')
    fig.text(0.01, 0.22, 'PowerFactory', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.05, hspace=0.4)

    plt.show()

def plot_iabc_zoom(pf_df, sim_df, t_start=11.4, t_end=11.6, f_time=None):
    """
    Plots Iabc from PowerFactory and Simulink in a 1x2 layout for a given time window.

    Parameters:
        pf_df, sim_df: DataFrames with 'time', 'i_a', 'i_b', 'i_c'
        t_start, t_end: time window to zoom in on
    """
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 2}
    # Filter window
    pf_win = pf_df[(pf_df['time'] >= t_start) & (pf_df['time'] <= t_end)]
    sim_win = sim_df[(sim_df['time'] >= t_start) & (sim_df['time'] <= t_end)]

    fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
    fig.suptitle(f'Iabc Comparison ({t_start}s – {t_end}s)', fontsize=14)

    # PowerFactory
    axs[0].plot(pf_win['time'], pf_win['i_a'], label='Ia', color='tab:blue')
    axs[0].plot(pf_win['time'], pf_win['i_b'], label='Ib', color='tab:green')
    axs[0].plot(pf_win['time'], pf_win['i_c'], label='Ic', color='tab:orange')
    axs[0].set_title('PowerFactory')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Current [A or kA] ?')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].axvline(f_time, **line_style)

    # Simulink
    axs[1].plot(sim_win['time'], sim_win['i_a'], label='Ia', color='tab:blue')
    axs[1].plot(sim_win['time'], sim_win['i_b'], label='Ib', color='tab:green')
    axs[1].plot(sim_win['time'], sim_win['i_c'], label='Ic', color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('Current pu')
    axs[1].set_xlabel('Time [s]')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].axvline(f_time, **line_style)

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

def plot_iabc_dual_zoom(pf_df, sim_df, t1_start, t1_end, t2_start, t2_end, f_time1=None, f_time2=None):
    """
    Compares Iabc from Simulink and PowerFactory in two time windows.
    Arranged in a 2x2 grid: [Sim-start | Sim-end], [PF-start | PF-end]
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 6), sharey=False)
    fig.suptitle('Iabc Comparison (Two Time Windows)', fontsize=16)
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}

    # --- Window 1: Simulink ---
    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    axs[0, 0].plot(sim1['time'], sim1['i_a'], label='Ia', color='tab:blue')
    axs[0, 0].plot(sim1['time'], sim1['i_b'], label='Ib', color='tab:green')
    axs[0, 0].plot(sim1['time'], sim1['i_c'], label='Ic', color='tab:orange')
    axs[0, 0].set_title(f'Simulink ({t1_start}s–{t1_end}s)')
    axs[0, 0].set_ylabel('Current [pu]')
    axs[0, 0].grid(True)
    if f_time1:
        axs[0, 0].axvline(f_time1, **line_style)
    axs[0, 0].legend()

    # --- Window 2: Simulink ---
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    axs[0, 1].plot(sim2['time'], sim2['i_a'], label='Ia', color='tab:blue')
    axs[0, 1].plot(sim2['time'], sim2['i_b'], label='Ib', color='tab:green')
    axs[0, 1].plot(sim2['time'], sim2['i_c'], label='Ic', color='tab:orange')
    axs[0, 1].set_title(f'Simulink ({t2_start}s–{t2_end}s)')
    axs[0, 1].grid(True)
    if f_time2:
        axs[0, 1].axvline(f_time2, **line_style)

    # --- Window 1: PowerFactory ---
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    axs[1, 0].plot(pf1['time'], pf1['i_a'], label='Ia', color='tab:blue')
    axs[1, 0].plot(pf1['time'], pf1['i_b'], label='Ib', color='tab:green')
    axs[1, 0].plot(pf1['time'], pf1['i_c'], label='Ic', color='tab:orange')
    axs[1, 0].set_title(f'PowerFactory ({t1_start}s–{t1_end}s)')
    axs[1, 0].set_ylabel('Current pu')
    axs[1, 0].set_xlabel('Time [s]')
    axs[1, 0].grid(True)
    if f_time1:
        axs[1, 0].axvline(f_time1, **line_style)

    # --- Window 2: PowerFactory ---
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    axs[1, 1].plot(pf2['time'], pf2['i_a'], label='Ia', color='tab:blue')
    axs[1, 1].plot(pf2['time'], pf2['i_b'], label='Ib', color='tab:green')
    axs[1, 1].plot(pf2['time'], pf2['i_c'], label='Ic', color='tab:orange')
    axs[1, 1].set_title(f'PowerFactory ({t2_start}s–{t2_end}s)')
    axs[1, 1].set_xlabel('Time [s]')
    axs[1, 1].grid(True)
    if f_time2:
        axs[1, 1].axvline(f_time2, **line_style)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()



def plot_power_zoom(pf_df, sim_df, param='p_kw', t_start=11.4, t_end=11.6, f_time=None):
    """
    Plots active or reactive power from PowerFactory and Simulink in a 1x2 layout.

    Parameters:
        pf_df, sim_df: DataFrames with 'time' and power column (e.g., 'p_kw' or 'q_kw')
        param: which column to plot ('p_kw' or 'q_kw')
        t_start, t_end: time window to zoom in on
        f_time: optional fault/event marker time (vertical dashed line)
    """
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 2}
    pf_win = pf_df[(pf_df['time'] >= t_start) & (pf_df['time'] <= t_end)]
    sim_win = sim_df[(sim_df['time'] >= t_start) & (sim_df['time'] <= t_end)]

    # Label guess based on parameter
    label = 'Active Power [kW]' if 'p' in param else 'Reactive Power [kVar]'
    title = 'Active Power' if 'p' in param else 'Reactive Power'

    fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
    fig.suptitle(f'{title} Comparison ({t_start}s – {t_end}s)', fontsize=14)

    # PowerFactory
    axs[0].plot(pf_win['time'], pf_win[param], color='tab:blue')
    axs[0].set_title('PowerFactory')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel(label)
    axs[0].grid(True)
    if f_time:
        axs[0].axvline(f_time, **line_style)

    # Simulink
    axs[1].plot(sim_win['time'], sim_win[param], color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel(label)
    axs[1].grid(True)
    if f_time:
        axs[1].axvline(f_time, **line_style)

    plt.tight_layout()
    plt.show()
    
    
import matplotlib.pyplot as plt

def plot_power_dual_zoom(pf_df, sim_df, param='p_kw',
                         t1_start=11.4, t1_end=11.6,
                         t2_start=11.9, t2_end=12.3,
                         f_time1=None, f_time2=None):
    """
    Plots active or reactive power from Simulink and PowerFactory across two time windows.
    2x2 layout: [Sim-start | Sim-end], [PF-start | PF-end]

    Parameters:
        pf_df, sim_df: DataFrames with 'time' and power column (e.g., 'p_kw' or 'q_kw')
        param: column name to plot
        t*_start, t*_end: start/end of the two time windows
        f_time1, f_time2: fault marker lines for each window
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 6), sharey=False)
    fig.suptitle(f"{'Active' if 'p' in param else 'Reactive'} Power Comparison", fontsize=16)
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}

    # Labels
    label = 'Active Power [kW]' if 'p' in param else 'Reactive Power [kVar]'

    # --- Simulink Window 1 ---
    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    axs[0, 0].plot(sim1['time'], sim1[param], color='tab:orange')
    axs[0, 0].set_title(f'Simulink ({t1_start}s–{t1_end}s)')
    axs[0, 0].set_ylabel(label)
    axs[0, 0].grid(True)
    if f_time1:
        axs[0, 0].axvline(f_time1, **line_style)

    # --- Simulink Window 2 ---
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    axs[0, 1].plot(sim2['time'], sim2[param], color='tab:orange')
    axs[0, 1].set_title(f'Simulink ({t2_start}s–{t2_end}s)')
    axs[0, 1].grid(True)
    if f_time2:
        axs[0, 1].axvline(f_time2, **line_style)

    # --- PowerFactory Window 1 ---
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    axs[1, 0].plot(pf1['time'], pf1[param], color='tab:blue')
    axs[1, 0].set_title(f'PowerFactory ({t1_start}s–{t1_end}s)')
    axs[1, 0].set_xlabel('Time [s]')
    axs[1, 0].set_ylabel(label)
    axs[1, 0].grid(True)
    if f_time1:
        axs[1, 0].axvline(f_time1, **line_style)

    # --- PowerFactory Window 2 ---
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    axs[1, 1].plot(pf2['time'], pf2[param], color='tab:blue')
    axs[1, 1].set_title(f'PowerFactory ({t2_start}s–{t2_end}s)')
    axs[1, 1].set_xlabel('Time [s]')
    axs[1, 1].grid(True)
    if f_time2:
        axs[1, 1].axvline(f_time2, **line_style)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()






def plot_vabc_grid(pf_df, sim_df,
                   t1_start=11.4, t1_end=11.6,
                   t2_start=11.9, t2_end=12.3,
                   t3_start=10.0, t3_end=13.5,
                   f_time1=None, f_time2=None):
    """
    Plots Vabc for Simulink and PowerFactory in a 4x2 layout:
    Row 1: Simulink full span
    Row 2: Simulink zoomed start | end
    Row 3: PowerFactory zoomed start | end
    Row 4: PowerFactory full span
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    from matplotlib import gridspec

    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}
    line_style2 = {'color': 'black', 'linestyle': '-', 'linewidth': 1.5}

    fig = plt.figure(figsize=(12, 10))
    fig.suptitle("Vabc", fontsize=16)

    # Horizontal divider between sections
    fig.add_artist(plt.Line2D([0, 1], [0.475, 0.475], color='black', linewidth=1.0, linestyle='-'))

    # 4x2 grid layout
    gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1])

    # === Full Simulink (Top Row) ===
    sim_full_ish = sim_df[(sim_df['time'] >= t3_start) & (sim_df['time'] <= t3_end)]
    ax_sim_full = fig.add_subplot(gs[0, :])
    for phase, color in zip(['v_a', 'v_b', 'v_c'], ['tab:blue', 'tab:green', 'tab:orange']):
        ax_sim_full.plot(sim_full_ish['time'], sim_full_ish[phase], label=phase.replace('v_', 'V'), color=color, zorder=0)
    ax_sim_full.set_ylabel('Voltage pu')
    ax_sim_full.grid(True)
    ax_sim_full.legend(loc='upper right')
    for label, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label else line_style2
            ax_sim_full.axvline(line_time, **style)

    ax_sim_full.set_xlim([t3_start, t3_end])

    # === Simulink Zoomed Plots ===
    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    ax_sim_start, ax_sim_end = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
    ax_sim_start.zorder = 3
    ax_sim_end.zorder = 3

    for ax, data in zip([ax_sim_start, ax_sim_end], [sim1, sim2]):
        for phase, color in zip(['v_a', 'v_b', 'v_c'], ['tab:blue', 'tab:green', 'tab:orange']):
            ax.plot(data['time'], data[phase], color=color)
        ax.grid(True)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])
        for label, line_time in zip(
            ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
            [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
        ):
            if line_time is not None:
                style = line_style if 'f_time' in label else line_style2
                ax.axvline(line_time, **style)

    ax_sim_start.set_ylabel('Voltage pu')

    # === PowerFactory Zoomed Plots ===
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    ax_pf_start, ax_pf_end = fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[2, 1])
    ax_pf_start.zorder = 3
    ax_pf_end.zorder = 3

    for ax, data in zip([ax_pf_start, ax_pf_end], [pf1, pf2]):
        for phase, color in zip(['v_a', 'v_b', 'v_c'], ['tab:blue', 'tab:green', 'tab:orange']):
            ax.plot(data['time'], data[phase], color=color)
        ax.grid(True)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])
        for label, line_time in zip(
            ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
            [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
        ):
            if line_time is not None:
                style = line_style if 'f_time' in label else line_style2
                ax.axvline(line_time, **style)

    ax_pf_start.set_ylabel('Voltage pu')

    # === Full PowerFactory Plot ===
    pf_full_ish = pf_df[(pf_df['time'] >= t3_start) & (pf_df['time'] <= t3_end)]
    ax_pf_full = fig.add_subplot(gs[3, :])
    for phase, color in zip(['v_a', 'v_b', 'v_c'], ['tab:blue', 'tab:green', 'tab:orange']):
        ax_pf_full.plot(pf_full_ish['time'], pf_full_ish[phase], label=phase.replace('v_', 'V'), color=color, zorder=0)
    ax_pf_full.set_ylabel('Voltage pu')
    ax_pf_full.set_xlabel('Time [s]')
    ax_pf_full.grid(True)
    ax_pf_full.legend(loc='upper right')
    for label, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label else line_style2
            ax_pf_full.axvline(line_time, **style)

    ax_pf_full.set_xlim([t3_start, t3_end])

    # Add vertical labels
    fig.text(0.01, 0.78, 'Simulink', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')
    fig.text(0.01, 0.22, 'PowerFactory', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')

    # Adjust layout before connections
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.05, hspace=0.4)

    # === Connect Zooms to Full Views ===
    for ax_zoom, data, full_ax in [
        (ax_sim_start, sim1, ax_sim_full),
        (ax_sim_end, sim2, ax_sim_full),
        (ax_pf_start, pf1, ax_pf_full),
        (ax_pf_end, pf2, ax_pf_full)
    ]:
        y_zoom_min, y_zoom_max = ax_zoom.get_ylim()
        y_full_min, y_full_max = full_ax.get_ylim()
        x_start = data['time'].iloc[0]
        x_end = data['time'].iloc[-1]

        corners_zoom = [(x_start, y_zoom_min), (x_start, y_zoom_max),
                        (x_end, y_zoom_min),   (x_end, y_zoom_max)]
        corners_full = [(x_start, y_full_min), (x_start, y_full_max),
                        (x_end, y_full_min),   (x_end, y_full_max)]

        for (xA, yA), (xB, yB) in zip(corners_zoom, corners_full):
            con = ConnectionPatch(
                xyA=(xA, yA), coordsA=ax_zoom.transData,
                xyB=(xB, yB), coordsB=full_ax.transData,
                axesA=ax_zoom, axesB=full_ax,
                color='gray', linestyle='--', linewidth=0.8, zorder=2
            )
            fig.add_artist(con)
            
    for ax in [ax_sim_start, ax_sim_end, ax_pf_start, ax_pf_end]:
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)  # or any value you like
            
        
    for ax in [ax_sim_full, ax_pf_full]:
        for (x0, x1) in [(t1_start, t1_end), (t2_start, t2_end)]:
            # top line
            ax.plot([x0, x1], [1, 1], transform=ax.get_xaxis_transform(), clip_on=False, **line_style2)
            # bottom line
            ax.plot([x0, x1], [0, 0], transform=ax.get_xaxis_transform(), **line_style2)


    plt.show()


def plot_iabc_grid(pf_df, sim_df,
                   t1_start=11.4, t1_end=11.6,
                   t2_start=11.9, t2_end=12.3,
                   t3_start=10.0, t3_end=13.5,
                   f_time1=None, f_time2=None):
    """
    Plots Iabc for Simulink and PowerFactory in a 4x2 layout:
    Row 1: Simulink full span
    Row 2: Simulink zoomed start | end
    Row 3: PowerFactory zoomed start | end
    Row 4: PowerFactory full span
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    from matplotlib import gridspec

    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}
    line_style2 = {'color': 'black', 'linestyle': '-', 'linewidth':1.5}

    fig = plt.figure(figsize=(12, 10))
    fig.suptitle("Iabc", fontsize=16)

    # Horizontal divider between sections
    fig.add_artist(plt.Line2D([0, 1], [0.475, 0.475], color='black', linewidth=1.0, linestyle='-'))

    # 4x2 grid layout
    gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1])

    # === Full Simulink (Top Row) ===
    sim_full_ish = sim_df[(sim_df['time'] >= t3_start) & (sim_df['time'] <= t3_end)]
    ax_sim_full = fig.add_subplot(gs[0, :])
    for phase, color in zip(['i_a', 'i_b', 'i_c'], ['tab:blue', 'tab:green', 'tab:orange']):
        ax_sim_full.plot(sim_full_ish['time'], sim_full_ish[phase], label=phase.replace('i_', 'I'), color=color, zorder=0)
    ax_sim_full.set_ylabel('Current pu')
    ax_sim_full.grid(True)
    ax_sim_full.legend(loc='upper right')
    for label, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label else line_style2
            ax_sim_full.axvline(line_time, **style)
    ax_sim_full.set_xlim([t3_start, t3_end])

    # === Simulink Zoomed Plots ===
    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    ax_sim_start, ax_sim_end = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
    ax_sim_start.zorder = 3
    ax_sim_end.zorder = 3

    for ax, data in zip([ax_sim_start, ax_sim_end], [sim1, sim2]):
        for phase, color in zip(['i_a', 'i_b', 'i_c'], ['tab:blue', 'tab:green', 'tab:orange']):
            ax.plot(data['time'], data[phase], color=color)
        ax.grid(True)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])
        for label, line_time in zip(
            ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
            [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
        ):
            if line_time is not None:
                style = line_style if 'f_time' in label else line_style2
                ax.axvline(line_time, **style)
    ax_sim_start.set_ylabel('Current pu')

    # === PowerFactory Zoomed Plots ===
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    ax_pf_start, ax_pf_end = fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[2, 1])
    ax_pf_start.zorder = 3
    ax_pf_end.zorder = 3

    for ax, data in zip([ax_pf_start, ax_pf_end], [pf1, pf2]):
        for phase, color in zip(['i_a', 'i_b', 'i_c'], ['tab:blue', 'tab:green', 'tab:orange']):
            ax.plot(data['time'], data[phase], color=color)
        ax.grid(True)
        ax.set_xlim([data['time'].iloc[0], data['time'].iloc[-1]])
        for label, line_time in zip(
            ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
            [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
        ):
            if line_time is not None:
                style = line_style if 'f_time' in label else line_style2
                ax.axvline(line_time, **style)
    ax_pf_start.set_ylabel('Current pu')

    # === Full PowerFactory Plot ===
    pf_full_ish = pf_df[(pf_df['time'] >= t3_start) & (pf_df['time'] <= t3_end)]
    ax_pf_full = fig.add_subplot(gs[3, :])
    for phase, color in zip(['i_a', 'i_b', 'i_c'], ['tab:blue', 'tab:green', 'tab:orange']):
        ax_pf_full.plot(pf_full_ish['time'], pf_full_ish[phase], label=phase.replace('i_', 'I'), color=color, zorder=0)
    ax_pf_full.set_ylabel('Current pu')
    ax_pf_full.set_xlabel('Time [s]')
    ax_pf_full.grid(True)
    ax_pf_full.legend(loc='upper right')
    for label, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label else line_style2
            ax_pf_full.axvline(line_time, **style)
    ax_pf_full.set_xlim([t3_start, t3_end])

    # Add vertical labels
    fig.text(0.01, 0.78, 'Simulink', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')
    fig.text(0.01, 0.22, 'PowerFactory', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')

    # Adjust layout before connections
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.05, hspace=0.4)

    # === Connect Zooms to Full Views ===
    for ax_zoom, data, full_ax in [
        (ax_sim_start, sim1, ax_sim_full),
        (ax_sim_end, sim2, ax_sim_full),
        (ax_pf_start, pf1, ax_pf_full),
        (ax_pf_end, pf2, ax_pf_full)
    ]:
        y_zoom_min, y_zoom_max = ax_zoom.get_ylim()
        y_full_min, y_full_max = full_ax.get_ylim()
        x_start = data['time'].iloc[0]
        x_end = data['time'].iloc[-1]

        corners_zoom = [(x_start, y_zoom_min), (x_start, y_zoom_max),
                        (x_end, y_zoom_min),   (x_end, y_zoom_max)]
        corners_full = [(x_start, y_full_min), (x_start, y_full_max),
                        (x_end, y_full_min),   (x_end, y_full_max)]

        for (xA, yA), (xB, yB) in zip(corners_zoom, corners_full):
            con = ConnectionPatch(
                xyA=(xA, yA), coordsA=ax_zoom.transData,
                xyB=(xB, yB), coordsB=full_ax.transData,
                axesA=ax_zoom, axesB=full_ax,
                color='gray', linestyle='--', linewidth=0.8, zorder=2
            )
            fig.add_artist(con)
            
    for ax in [ax_sim_start, ax_sim_end, ax_pf_start, ax_pf_end]:
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)  # or any value you like
            
        
    for ax in [ax_sim_full, ax_pf_full]:
        for (x0, x1) in [(t1_start, t1_end), (t2_start, t2_end)]:
            # top line
            ax.plot([x0, x1], [1, 1], transform=ax.get_xaxis_transform(), clip_on=False, **line_style2)
            # bottom line
            ax.plot([x0, x1], [0, 0], transform=ax.get_xaxis_transform(), **line_style2)


    plt.show()


def plot_power_grid(pf_df, sim_df,
                    col='p_kw',
                    label='Active Power [kW]',
                    title='Active Power',
                    t1_start=11.4, t1_end=11.6,
                    t2_start=11.9, t2_end=12.3,
                    t3_start=10.0, t3_end=13.5,
                    f_time1=None, f_time2=None):
    """
    Plots active or reactive power from PowerFactory and Simulink in a 4x2 layout:
    Row 1: Simulink full span
    Row 2: Simulink zoomed start | end
    Row 3: PowerFactory zoomed start | end
    Row 4: PowerFactory full span
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    from matplotlib import gridspec

    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}
    line_style2 = {'color': 'black', 'linestyle': '-', 'linewidth': 1.5}

    fig = plt.figure(figsize=(12, 10))
    fig.suptitle(title, fontsize=16)

    fig.add_artist(plt.Line2D([0, 1], [0.475, 0.475], color='black', linewidth=1.0, linestyle='-'))
    gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1])

    sim_full = sim_df[(sim_df['time'] >= t3_start) & (sim_df['time'] <= t3_end)]
    ax_sim_full = fig.add_subplot(gs[0, :])
    ax_sim_full.zorder = 0
    ax_sim_full.plot(sim_full['time'], sim_full[col], color='tab:blue', zorder=0)
    ax_sim_full.set_ylabel(label)
    ax_sim_full.grid(True)
    ax_sim_full.set_xlim([t3_start, t3_end])
    for label_tag, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label_tag else line_style2
            ax_sim_full.axvline(line_time, **style)

    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    ax_sim_start = fig.add_subplot(gs[1, 0])
    ax_sim_start.zorder = 3
    ax_sim_end = fig.add_subplot(gs[1, 1])
    ax_sim_end.zorder = 3
    ax_sim_start.plot(sim1['time'], sim1[col], color='tab:blue')
    ax_sim_end.plot(sim2['time'], sim2[col], color='tab:blue')
    ax_sim_start.grid(True)
    ax_sim_end.grid(True)
    ax_sim_start.set_xlim([t1_start, t1_end])
    ax_sim_end.set_xlim([t2_start, t2_end])
    ax_sim_start.set_ylabel(label)
    for ax, lines in zip([ax_sim_start, ax_sim_end], [[f_time1, t1_start, t1_end], [f_time2, t2_start, t2_end]]):
        for l, tag in zip(lines, ['f_time', 't_start', 't_end']):
            if l is not None:
                style = line_style if 'f_time' in tag else line_style2
                ax.axvline(l, **style)

    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    ax_pf_start = fig.add_subplot(gs[2, 0])
    ax_pf_start.zorder = 3
    ax_pf_end = fig.add_subplot(gs[2, 1])
    ax_pf_end.zorder = 3
    ax_pf_start.plot(pf1['time'], pf1[col], color='tab:blue')
    ax_pf_end.plot(pf2['time'], pf2[col], color='tab:blue')
    ax_pf_start.grid(True)
    ax_pf_end.grid(True)
    ax_pf_start.set_xlim([t1_start, t1_end])
    ax_pf_end.set_xlim([t2_start, t2_end])
    ax_pf_start.set_ylabel(label)
    for ax, lines in zip([ax_pf_start, ax_pf_end], [[f_time1, t1_start, t1_end], [f_time2, t2_start, t2_end]]):
        for l, tag in zip(lines, ['f_time', 't_start', 't_end']):
            if l is not None:
                style = line_style if 'f_time' in tag else line_style2
                ax.axvline(l, **style)

    pf_full = pf_df[(pf_df['time'] >= t3_start) & (pf_df['time'] <= t3_end)]
    ax_pf_full = fig.add_subplot(gs[3, :])
    ax_pf_full.plot(pf_full['time'], pf_full[col], color='tab:blue', zorder=0)
    ax_pf_full.set_ylabel(label)
    ax_pf_full.set_xlabel('Time [s]')
    ax_pf_full.grid(True)
    ax_pf_full.set_xlim([t3_start, t3_end])
    for label_tag, line_time in zip(
        ['f_time1', 'f_time2', 't1_start', 't1_end', 't2_start', 't2_end'],
        [f_time1, f_time2, t1_start, t1_end, t2_start, t2_end]
    ):
        if line_time is not None:
            style = line_style if 'f_time' in label_tag else line_style2
            ax_pf_full.axvline(line_time, **style)

    fig.text(0.01, 0.78, 'Simulink', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')
    fig.text(0.01, 0.22, 'PowerFactory', fontsize=12, fontweight='bold', va='center', ha='center', rotation='vertical')

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.05, hspace=0.4)

    # === Connect Zooms to Full Views ===
    for ax_zoom, data, full_ax in [
        (ax_sim_start, sim1, ax_sim_full),
        (ax_sim_end, sim2, ax_sim_full),
        (ax_pf_start, pf1, ax_pf_full),
        (ax_pf_end, pf2, ax_pf_full)
    ]:
        y_zoom_min, y_zoom_max = ax_zoom.get_ylim()
        y_full_min, y_full_max = full_ax.get_ylim()
        x_start = data['time'].iloc[0]
        x_end = data['time'].iloc[-1]

        corners_zoom = [(x_start, y_zoom_min), (x_start, y_zoom_max),
                        (x_end, y_zoom_min),   (x_end, y_zoom_max)]
        corners_full = [(x_start, y_full_min), (x_start, y_full_max),
                        (x_end, y_full_min),   (x_end, y_full_max)]

        for (xA, yA), (xB, yB) in zip(corners_zoom, corners_full):
            con = ConnectionPatch(
                xyA=(xA, yA), coordsA=ax_zoom.transData,
                xyB=(xB, yB), coordsB=full_ax.transData,
                axesA=ax_zoom, axesB=full_ax,
                color='gray', linestyle='--', linewidth=0.8, zorder=2
            )
            fig.add_artist(con)

    for ax in [ax_sim_start, ax_sim_end, ax_pf_start, ax_pf_end]:
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)  # or any value you like
            
        
    for ax in [ax_sim_full, ax_pf_full]:
        for (x0, x1) in [(t1_start, t1_end), (t2_start, t2_end)]:
            # top line
            ax.plot([x0, x1], [1, 1], transform=ax.get_xaxis_transform(), clip_on=False, **line_style2)
            # bottom line
            ax.plot([x0, x1], [0, 0], transform=ax.get_xaxis_transform(), **line_style2)



    plt.show()
    
    
def plot_p(pf_df, pwr_df, sim_df):
    """
    Plots active power (P) in kW from PowerFactory, PowerDynamics, and Simulink in a 3x1 subplot layout.
    Includes vertical lines at 11.5s and 12s for event markers.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    fig.suptitle('Active Power Comparison (P)', fontsize=16)

    event_times = [11.5, 12]
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1}

    # PowerFactory
    axs[0].plot(pf_df['time'], pf_df['p_kw'], color='tab:blue')
    axs[0].set_title('PowerFactory')
    axs[0].set_ylabel('P [kW]')
    axs[0].set_xlabel('Time [s]')
    axs[0].grid(True)
    for t in event_times:
        axs[0].axvline(x=t, **line_style)

    # # PowerDynamics
    # axs[1].plot(pwr_df['time'], pwr_df['p_kw'], color='tab:green')
    # axs[1].set_title('PowerDynamics')
    # axs[1].set_ylabel('P [kW]')
    # axs[1].set_xlabel('Time [s]')
    # axs[1].grid(True)
    # for t in event_times:
    #     axs[1].axvline(x=t, **line_style)

    # Simulink
    axs[1].plot(sim_df['time'], sim_df['p_kw'], color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('P [kW]')
    axs[1].set_xlabel('Time [s]')
    axs[1].grid(True)
    for t in event_times:
        axs[1].axvline(x=t, **line_style)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=2.0)
    plt.show()


def plot_q(pf_df, pwr_df, sim_df):
    """
    Plots active power (P) in kW from PowerFactory, PowerDynamics, and Simulink in a 3x1 subplot layout.
    Includes vertical lines at 11.5s and 12s for event markers.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    fig.suptitle('Reactive Power Comparison (Q)', fontsize=16)

    event_times = [11.5, 12]
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1}

    # PowerFactory
    axs[0].plot(pf_df['time'], pf_df['q_kw'], color='tab:blue')
    axs[0].set_title('PowerFactory')
    axs[0].set_ylabel('Q [kW]')
    axs[0].set_xlabel('Time [s]')
    axs[0].grid(True)
    for t in event_times:
        axs[0].axvline(x=t, **line_style)

    # # PowerDynamics
    # axs[1].plot(pwr_df['time'], pwr_df['p_kw'], color='tab:green')
    # axs[1].set_title('PowerDynamics')
    # axs[1].set_ylabel('P [kW]')
    # axs[1].set_xlabel('Time [s]')
    # axs[1].grid(True)
    # for t in event_times:
    #     axs[1].axvline(x=t, **line_style)

    # Simulink
    axs[1].plot(sim_df['time'], sim_df['q_kw'], color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('Q [kW]')
    axs[1].set_xlabel('Time [s]')
    axs[1].grid(True)
    for t in event_times:
        axs[1].axvline(x=t, **line_style)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=2.0)
    plt.show()


def plot_vabc(pf_df, pwr_df, sim_df):
    """
    Plots three-phase voltage (Vabc) from PowerFactory, PowerDynamics, and Simulink in a 3x1 layout.
    Includes vertical event lines at 11.5s and 12s.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    fig.suptitle('Three-Phase Voltage Comparison (Vabc)', fontsize=16)

    event_times = [11.5, 12]
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1}

    # PowerFactory
    axs[0].plot(pf_df['time'], pf_df['v_a'], label='Va', color='tab:orange')
    axs[0].plot(pf_df['time'], pf_df['v_b'], label='Vb', color='tab:green')
    axs[0].plot(pf_df['time'], pf_df['v_c'], label='Vc', color='tab:blue')
    axs[0].set_title('PowerFactory')
    axs[0].set_ylabel('V pu')
    axs[0].set_xlabel('Time [s]')
    axs[0].grid(True)
    for t in event_times:
        axs[0].axvline(x=t, **line_style)

    # # PowerDynamics
    # axs[1].plot(pwr_df['time'], pwr_df['v'], label='Va', color='tab:blue')
    # axs[1].set_title('PowerDynamics')
    # axs[1].set_ylabel('V pu')
    # axs[1].set_xlabel('Time [s]')
    # axs[1].grid(True)
    # for t in event_times:
    #     axs[1].axvline(x=t, **line_style)

    # Simulink
    axs[1].plot(sim_df['time'], sim_df['v_a'], label='Va', color='tab:blue')
    axs[1].plot(sim_df['time'], sim_df['v_b'], label='Vb', color='tab:green')
    axs[1].plot(sim_df['time'], sim_df['v_c'], label='Vc', color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('V pu')
    axs[1].set_xlabel('Time [s]')
    axs[1].grid(True)
    for t in event_times:
        axs[1].axvline(x=t, **line_style)

    # Only add legend once (or adjust as needed)
    axs[0].legend(loc='upper right')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=2.0)
    plt.show()


def plot_iabc(pf_df, sim_df):
    """
    Plots three-phase current (Iabc) from PowerFactory and Simulink in a 2x1 layout.
    Includes vertical event lines at 11.5s and 12s.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 5))
    fig.suptitle('Three-Phase Current Comparison (Iabc)', fontsize=16)

    event_times = [11.5, 12]
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1}

    # PowerFactory
    axs[0].plot(pf_df['time'], pf_df['i_a'], label='Ia', color='tab:orange')
    axs[0].plot(pf_df['time'], pf_df['i_b'], label='Ib', color='tab:green')
    axs[0].plot(pf_df['time'], pf_df['i_c'], label='Ic', color='tab:blue')
    axs[0].set_title('PowerFactory')
    axs[0].set_ylabel('I pu')
    axs[0].grid(True)
    for t in event_times:
        axs[0].axvline(x=t, **line_style)

    # Simulink
    axs[1].plot(sim_df['time'], sim_df['i_a'], label='Ia', color='tab:blue')
    axs[1].plot(sim_df['time'], sim_df['i_b'], label='Ib', color='tab:green')
    axs[1].plot(sim_df['time'], sim_df['i_c'], label='Ic', color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('I pu')
    axs[1].set_xlabel('Time [s]')
    axs[1].grid(True)
    for t in event_times:
        axs[1].axvline(x=t, **line_style)

    axs[0].legend(loc='upper right')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=2.0)
    plt.show()


def plot_vabc_zoom(pf_df, sim_df, t_start=11.4, t_end=11.6, f_time=None):
    """
    Plots Vabc from PowerFactory and Simulink in a 1x2 layout for a given time window.

    Parameters:
        pf_df, sim_df: DataFrames with 'time', 'v_a', 'v_b', 'v_c'
        t_start, t_end: time window to zoom in on
    """
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 2}
    # Filter window
    pf_win = pf_df[(pf_df['time'] >= t_start) & (pf_df['time'] <= t_end)]
    sim_win = sim_df[(sim_df['time'] >= t_start) & (sim_df['time'] <= t_end)]

    fig, axs = plt.subplots(4, 4, figsize=(12, 4), sharey=False)
    fig.suptitle(f'Vabc Comparison ({t_start}s – {t_end}s)', fontsize=14)

    # PowerFactory
    axs[0].plot(pf_win['time'], pf_win['v_a'], label='Va', color='tab:blue')
    axs[0].plot(pf_win['time'], pf_win['v_b'], label='Vb', color='tab:green')
    axs[0].plot(pf_win['time'], pf_win['v_c'], label='Vc', color='tab:orange')
    axs[0].set_title('PowerFactory')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Voltage pu')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].axvline(f_time, **line_style)

    # Simulink
    axs[1].plot(sim_win['time'], sim_win['v_a'], label='Va', color='tab:blue')
    axs[1].plot(sim_win['time'], sim_win['v_b'], label='Vb', color='tab:green')
    axs[1].plot(sim_win['time'], sim_win['v_c'], label='Vc', color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('Voltage pu')
    axs[1].set_xlabel('Time [s]')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].axvline(f_time, **line_style)

    plt.tight_layout()
    plt.show()
    
    
def plot_iabc_zoom(pf_df, sim_df, t_start=11.4, t_end=11.6, f_time=None):
    """
    Plots Iabc from PowerFactory and Simulink in a 1x2 layout for a given time window.

    Parameters:
        pf_df, sim_df: DataFrames with 'time', 'i_a', 'i_b', 'i_c'
        t_start, t_end: time window to zoom in on
    """
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 2}
    # Filter window
    pf_win = pf_df[(pf_df['time'] >= t_start) & (pf_df['time'] <= t_end)]
    sim_win = sim_df[(sim_df['time'] >= t_start) & (sim_df['time'] <= t_end)]

    fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
    fig.suptitle(f'Iabc Comparison ({t_start}s – {t_end}s)', fontsize=14)

    # PowerFactory
    axs[0].plot(pf_win['time'], pf_win['i_a'], label='Ia', color='tab:blue')
    axs[0].plot(pf_win['time'], pf_win['i_b'], label='Ib', color='tab:green')
    axs[0].plot(pf_win['time'], pf_win['i_c'], label='Ic', color='tab:orange')
    axs[0].set_title('PowerFactory')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Current [A or kA] ?')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].axvline(f_time, **line_style)

    # Simulink
    axs[1].plot(sim_win['time'], sim_win['i_a'], label='Ia', color='tab:blue')
    axs[1].plot(sim_win['time'], sim_win['i_b'], label='Ib', color='tab:green')
    axs[1].plot(sim_win['time'], sim_win['i_c'], label='Ic', color='tab:orange')
    axs[1].set_title('Simulink')
    axs[1].set_ylabel('Current pu')
    axs[1].set_xlabel('Time [s]')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].axvline(f_time, **line_style)

    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

def plot_iabc_dual_zoom(pf_df, sim_df, t1_start, t1_end, t2_start, t2_end, f_time1=None, f_time2=None):
    """
    Compares Iabc from Simulink and PowerFactory in two time windows.
    Arranged in a 2x2 grid: [Sim-start | Sim-end], [PF-start | PF-end]
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 6), sharey=False)
    fig.suptitle('Iabc Comparison (Two Time Windows)', fontsize=16)
    line_style = {'color': 'red', 'linestyle': '--', 'linewidth': 1.5}

    # --- Window 1: Simulink ---
    sim1 = sim_df[(sim_df['time'] >= t1_start) & (sim_df['time'] <= t1_end)]
    axs[0, 0].plot(sim1['time'], sim1['i_a'], label='Ia', color='tab:blue')
    axs[0, 0].plot(sim1['time'], sim1['i_b'], label='Ib', color='tab:green')
    axs[0, 0].plot(sim1['time'], sim1['i_c'], label='Ic', color='tab:orange')
    axs[0, 0].set_title(f'Simulink ({t1_start}s–{t1_end}s)')
    axs[0, 0].set_ylabel('Current [pu]')
    axs[0, 0].grid(True)
    if f_time1:
        axs[0, 0].axvline(f_time1, **line_style)
    axs[0, 0].legend()

    # --- Window 2: Simulink ---
    sim2 = sim_df[(sim_df['time'] >= t2_start) & (sim_df['time'] <= t2_end)]
    axs[0, 1].plot(sim2['time'], sim2['i_a'], label='Ia', color='tab:blue')
    axs[0, 1].plot(sim2['time'], sim2['i_b'], label='Ib', color='tab:green')
    axs[0, 1].plot(sim2['time'], sim2['i_c'], label='Ic', color='tab:orange')
    axs[0, 1].set_title(f'Simulink ({t2_start}s–{t2_end}s)')
    axs[0, 1].grid(True)
    if f_time2:
        axs[0, 1].axvline(f_time2, **line_style)

    # --- Window 1: PowerFactory ---
    pf1 = pf_df[(pf_df['time'] >= t1_start) & (pf_df['time'] <= t1_end)]
    axs[1, 0].plot(pf1['time'], pf1['i_a'], label='Ia', color='tab:blue')
    axs[1, 0].plot(pf1['time'], pf1['i_b'], label='Ib', color='tab:green')
    axs[1, 0].plot(pf1['time'], pf1['i_c'], label='Ic', color='tab:orange')
    axs[1, 0].set_title(f'PowerFactory ({t1_start}s–{t1_end}s)')
    axs[1, 0].set_ylabel('Current pu')
    axs[1, 0].set_xlabel('Time [s]')
    axs[1, 0].grid(True)
    if f_time1:
        axs[1, 0].axvline(f_time1, **line_style)

    # --- Window 2: PowerFactory ---
    pf2 = pf_df[(pf_df['time'] >= t2_start) & (pf_df['time'] <= t2_end)]
    axs[1, 1].plot(pf2['time'], pf2['i_a'], label='Ia', color='tab:blue')
    axs[1, 1].plot(pf2['time'], pf2['i_b'], label='Ib', color='tab:green')
    axs[1, 1].plot(pf2['time'], pf2['i_c'], label='Ic', color='tab:orange')
    axs[1, 1].set_title(f'PowerFactory ({t2_start}s–{t2_end}s)')
    axs[1, 1].set_xlabel('Time [s]')
    axs[1, 1].grid(True)
    if f_time2:
        axs[1, 1].axvline(f_time2, **line_style)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def process_vabc(df, label, fault_start =11.5, fault_end=12.0, recovery_threshold=0.8):
    time = df['time']
    va = pd.to_numeric(df['v_a'], errors='coerce')
    vb = pd.to_numeric(df['v_b'], errors='coerce')
    vc = pd.to_numeric(df['v_c'], errors='coerce')

    pre_fault = (time >= (fault_start - 0.3)) & (time < fault_start)
    va_norm = va / va[pre_fault].abs().mean()
    vb_norm = vb / vb[pre_fault].abs().mean()
    vc_norm = vc / vc[pre_fault].abs().mean()

    fault_mask = (time >= fault_start) & (time <= fault_end)
    print(f"{label} - Dip during fault:")
    print(f"  Va: {va_norm[fault_mask].min():.2f}, Vb: {vb_norm[fault_mask].min():.2f}, Vc: {vc_norm[fault_mask].min():.2f}")

    post_fault = time > fault_end
    lower = recovery_threshold
    upper = 2 - recovery_threshold

    def find_recovery(norm_signal):
        recovery = (norm_signal[post_fault].abs() > lower) & (norm_signal[post_fault].abs() < upper)
        if recovery.any():
            return time[post_fault].iloc[recovery.idxmax()] - fault_end
        else:
            return None

    rec_va = find_recovery(va_norm)
    rec_vb = find_recovery(vb_norm)
    rec_vc = find_recovery(vc_norm)

    print(f"{label} - Time to recover to {recovery_threshold*100:.0f}%:")
    for phase, rec in zip(['Va', 'Vb', 'Vc'], [rec_va, rec_vb, rec_vc]):
        if rec is not None:
            print(f"  {phase}: {rec:.3f} s")
        else:
            print(f"  {phase}: Did not recover")

    # Plotting
    plt.plot(time, va_norm, label=f'Va - {label}')
    plt.plot(time, vb_norm, label=f'Vb - {label}')
    plt.plot(time, vc_norm, label=f'Vc - {label}')
    plt.axvspan(fault_start, fault_end, color='red', alpha=0.2)
    plt.axhline(y=lower, color='gray', linestyle='--', linewidth=0.8)
    plt.axhline(y=upper, color='gray', linestyle='--', linewidth=0.8)

    # Mark recovery points
    for rec_time in [rec_va, rec_vb, rec_vc]:
        if rec_time:
            plt.axvline(x=fault_end + rec_time, linestyle=':', color='black', alpha=0.7)

    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [pu]')
    plt.title(f'Normalized Vabc - {label}')
    plt.legend()
    plt.grid(True)
    plt.show()


def process_iabc(df, label, fault_start =11.5, fault_end=12.0, recovery_threshold=0.8):
    time = df['time']
    ia = pd.to_numeric(df['i_a'], errors='coerce')
    ib = pd.to_numeric(df['i_b'], errors='coerce')
    ic = pd.to_numeric(df['i_c'], errors='coerce')

    pre_fault = (time >= (fault_start - 0.3)) & (time < fault_start)
    ia_norm = ia / ia[pre_fault].abs().mean()
    ib_norm = ib / ib[pre_fault].abs().mean()
    ic_norm = ic / ic[pre_fault].abs().mean()

    fault_mask = (time >= fault_start) & (time <= fault_end)
    print(f"{label} - Current dip during fault:")
    print(f"  Ia: {ia_norm[fault_mask].min():.2f}, Ib: {ib_norm[fault_mask].min():.2f}, Ic: {ic_norm[fault_mask].min():.2f}")

    post_fault = time > fault_end
    lower = recovery_threshold
    upper = 2 - recovery_threshold

    def find_recovery(norm_signal):
        recovery = (norm_signal[post_fault].abs() > lower) & (norm_signal[post_fault].abs() < upper)
        if recovery.any():
            return time[post_fault].iloc[recovery.idxmax()] - fault_end
        else:
            return None

    rec_ia = find_recovery(ia_norm)
    rec_ib = find_recovery(ib_norm)
    rec_ic = find_recovery(ic_norm)

    print(f"{label} - Time to recover current to {recovery_threshold*100:.0f}%:")
    for phase, rec in zip(['Ia', 'Ib', 'Ic'], [rec_ia, rec_ib, rec_ic]):
        if rec is not None:
            print(f"  {phase}: {rec:.3f} s")
        else:
            print(f"  {phase}: Did not recover")

    # Plotting
    plt.plot(time, ia_norm, label=f'Ia - {label}')
    plt.plot(time, ib_norm, label=f'Ib - {label}')
    plt.plot(time, ic_norm, label=f'Ic - {label}')
    plt.axvspan(fault_start, fault_end, color='red', alpha=0.2)
    plt.axhline(y=lower, color='gray', linestyle='--', linewidth=0.8)
    plt.axhline(y=upper, color='gray', linestyle='--', linewidth=0.8)

    for rec_time in [rec_ia, rec_ib, rec_ic]:
        if rec_time:
            plt.axvline(x=fault_end + rec_time, linestyle=':', color='black', alpha=0.7)

    plt.xlabel('Time [s]')
    plt.ylabel('Current [pu]')
    plt.title(f'Normalized Iabc - {label}')
    plt.legend()
    plt.grid(True)
    plt.show()

def process_active_power(df, label, fault_start =11.5, fault_end=12.0, recovery_threshold=0.8):
    time = df['time']
    p = pd.to_numeric(df['p'], errors='coerce')  # Adjust if column name is different

    # Normalize to pre-fault average
    pre_fault = (time >= (fault_start - 0.3)) & (time < fault_start)
    p_nom = p[pre_fault].mean()
    p_norm = p / p_nom

    fault_mask = (time >= fault_start) & (time <= fault_end)
    min_p = p_norm[fault_mask].min()
    print(f"{label} - Active Power drop during fault: min = {min_p:.2f} pu")

    post_fault = time > fault_end
    lower = recovery_threshold
    upper = 2 - recovery_threshold

    # Recovery detection
    recovery = (p_norm[post_fault] > lower) & (p_norm[post_fault] < upper)
    if recovery.any():
        recovery_time = time[post_fault].iloc[recovery.idxmax()] - fault_end
        print(f"{label} - Active Power recovered to {recovery_threshold*100:.0f}% in: {recovery_time:.3f} s")
    else:
        recovery_time = None
        print(f"{label} - Active Power did not recover to {recovery_threshold*100:.0f}%.")

    # Plotting
    plt.plot(time, p_norm, label=f'P - {label}', color='blue')
    plt.axvspan(fault_start, fault_end, color='red', alpha=0.2)
    plt.axhline(y=lower, color='gray', linestyle='--', linewidth=0.8)
    plt.axhline(y=upper, color='gray', linestyle='--', linewidth=0.8)
    if recovery_time:
        plt.axvline(x=fault_end + recovery_time, linestyle=':', color='black', alpha=0.7)

    plt.xlabel('Time [s]')
    plt.ylabel('Active Power [pu]')
    plt.title(f'Normalized Active Power - {label}')
    plt.legend()
    plt.grid(True)
    plt.show()
