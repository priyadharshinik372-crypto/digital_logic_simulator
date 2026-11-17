
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Digital Logic Simulator",
    page_icon="⚡",
    layout="wide"
)

# LOGIC GATE FUNCTIONS
def logic_gate(gate, a, b=0):

    if gate == "AND":
        return a & b
    elif gate == "OR":
        return a | b
    elif gate == "NOT":
        return 1 - a
    elif gate == "NAND":
        return 1 - (a & b)
    elif gate == "NOR":
        return 1 - (a | b)
    elif gate == "XOR":
        return a ^ b
    elif gate == "XNOR":
        return 1 - (a ^ b)


# TRUTH TABLE GENERATOR
def generate_truth_table(gate):

    data = []

    if gate == "NOT":
        for a in [0, 1]:
            data.append({
                "Input A": a,
                "Output": logic_gate(gate, a)
            })

    else:
        for a, b in product([0, 1], repeat=2):
            data.append({
                "Input A": a,
                "Input B": b,
                "Output": logic_gate(gate, a, b)
            })

    return pd.DataFrame(data)


# HALF ADDER
def half_adder(a, b):

    sum_output = a ^ b
    carry_output = a & b

    return sum_output, carry_output


# FULL ADDER
def full_adder(a, b, cin):

    sum_output = a ^ b ^ cin

    carry_output = (
        (a & b) |
        (b & cin) |
        (a & cin)
    )

    return sum_output, carry_output


# SIDEBAR MENU
st.sidebar.title("⚡ DIGITAL LOGIC")
st.sidebar.write("Circuit Design and Simulation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Logic Gate Simulator",
        "Truth Table Generator",
        "Half Adder",
        "Full Adder",
        "Circuit Visualization",
        "About Project"
    ]
)


# HOME DASHBOARD
if page == "Home":

    st.title("⚡ Digital Logic Circuit Simulator")

    st.subheader("Welcome to Our Project")

    st.write(
        "An Interactive Digital Logic Circuit "
        "Design and Simulation System using Python."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Logic Gates", "7")
    col2.metric("Adders", "2")
    col3.metric("Modules", "7")

    st.markdown("---")

    st.subheader("Project Features")

    st.success("Seven Basic Logic Gates")
    st.success("Automatic Truth Table Generator")
    st.success("Half Adder Simulation")
    st.success("Full Adder Simulation")
    st.success("Circuit Visualization")


# LOGIC GATE SIMULATOR
elif page == "Logic Gate Simulator":

    st.title("Logic Gate Simulator")

    gate = st.selectbox(
        "Select Logic Gate",
        ["AND", "OR", "NOT", "NAND",
         "NOR", "XOR", "XNOR"]
    )

    a = st.selectbox("Input A", [0, 1])

    if gate != "NOT":
        b = st.selectbox("Input B", [0, 1])
    else:
        b = 0

    result = logic_gate(gate, a, b)

    col1, col2, col3 = st.columns(3)

    col1.metric("Input A", a)

    if gate != "NOT":
        col2.metric("Input B", b)

    col3.metric("Output", result)

    if result == 1:
        st.success("Output HIGH (ON)")
    else:
        st.warning("Output LOW (OFF)")


# TRUTH TABLE GENERATOR
elif page == "Truth Table Generator":

    st.title("Truth Table Generator")

    gate = st.selectbox(
        "Select Logic Gate",
        ["AND", "OR", "NOT", "NAND",
         "NOR", "XOR", "XNOR"]
    )

    df = generate_truth_table(gate)

    st.subheader(gate + " Gate Truth Table")

    st.dataframe(df, use_container_width=True)

    st.write("Total Combinations:", len(df))


# HALF ADDER
elif page == "Half Adder":

    st.title("Half Adder Simulation")

    a = st.selectbox("Input A", [0, 1])
    b = st.selectbox("Input B", [0, 1])

    s, c = half_adder(a, b)

    col1, col2 = st.columns(2)

    col1.metric("SUM", s)
    col2.metric("CARRY", c)

    data = []

    for x, y in product([0, 1], repeat=2):

        sum_value, carry_value = half_adder(x, y)

        data.append({
            "A": x,
            "B": y,
            "Sum": sum_value,
            "Carry": carry_value
        })

    st.subheader("Half Adder Truth Table")

    st.dataframe(pd.DataFrame(data))


# FULL ADDER
elif page == "Full Adder":

    st.title("Full Adder Simulation")

    a = st.selectbox("Input A", [0, 1])
    b = st.selectbox("Input B", [0, 1])
    cin = st.selectbox("Carry Input", [0, 1])

    s, c = full_adder(a, b, cin)

    col1, col2 = st.columns(2)

    col1.metric("SUM", s)
    col2.metric("CARRY OUTPUT", c)

    data = []

    for x, y, z in product([0, 1], repeat=3):

        sum_value, carry_value = full_adder(x, y, z)

        data.append({
            "A": x,
            "B": y,
            "Carry In": z,
            "Sum": sum_value,
            "Carry Out": carry_value
        })

    st.subheader("Full Adder Truth Table")

    st.dataframe(pd.DataFrame(data))


# CIRCUIT VISUALIZATION
elif page == "Circuit Visualization":

    st.title("Circuit Visualization")

    circuit = st.selectbox(
        "Select Circuit",
        ["AND Gate", "OR Gate", "XOR Gate",
         "Half Adder", "Full Adder"]
    )

    fig, ax = plt.subplots(figsize=(9, 3))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    if circuit == "AND Gate":
        blocks = ["AND"]

    elif circuit == "OR Gate":
        blocks = ["OR"]

    elif circuit == "XOR Gate":
        blocks = ["XOR"]

    elif circuit == "Half Adder":
        blocks = ["XOR (SUM)", "AND (CARRY)"]

    else:
        blocks = ["XOR 1", "XOR 2", "Carry Logic"]

    ax.set_title(circuit + " Circuit Diagram")

    for i, block in enumerate(blocks):

        x = 1 + i * 3

        ax.text(
            x, 2.5, block,
            fontsize=13,
            ha="center",
            bbox=dict(
                boxstyle="round",
                facecolor="lightblue",
                edgecolor="navy"
            )
        )

        if i < len(blocks) - 1:
            ax.annotate(
                "",
                xy=(x + 2.5, 2.5),
                xytext=(x + 0.8, 2.5),
                arrowprops=dict(arrowstyle="->")
            )

    st.pyplot(fig)
    plt.close(fig)

    st.info("Simplified circuit block visualization.")


# ABOUT PROJECT
elif page == "About Project":

    st.title("About Project")

    st.subheader(
        "Digital Logic Circuit Design and Simulation System"
    )

    st.write(
        "This project simulates digital logic gates "
        "and arithmetic circuits using Python."
    )

    st.subheader("Technologies Used")

    st.write("1. Python")
    st.write("2. Streamlit")
    st.write("3. Pandas")
    st.write("4. Matplotlib")

    st.subheader("Subject Details")

    st.write("Subject: Computer System and Architecture")
    st.write("Subject Code: 231AD32")
    st.write("Project Type: Mini Project")

    st.success("Thank You!")
