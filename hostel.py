import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Balanced CGPA Grouping", layout="centered")
st.title("🎓 Balanced Group Formation Based on CGPA")

# Step 1: Get number of participants
num_participants = st.number_input("Enter number of participants", min_value=1, step=1)

cgpas = []
if num_participants > 0:
    st.subheader("Enter CGPA of Each Participant")
    for i in range(num_participants):
        cgpa = st.number_input(f"CGPA of Participant {i+1}", min_value=0.0, max_value=10.0, step=0.01)
        cgpas.append(cgpa)

# Step 2: Get number of desired groups
num_groups = st.number_input("Enter desired number of groups", min_value=1, step=1)

# On submission
if st.button("Generate Groups"):
    max_groups_possible = num_participants  # at least 1 per group
    min_groups_possible = int(np.ceil(num_participants / 4))  # max 4 per group

    if num_groups < min_groups_possible:
        st.warning(f"⚠️ Minimum number of groups required is {min_groups_possible} (to allow max 4 per group). Adjusting.")
        num_groups = min_groups_possible

    elif num_groups > max_groups_possible:
        st.warning(f"⚠️ You requested more groups than participants. Adjusting to {num_participants}.")
        num_groups = num_participants

    # Create list of (name, CGPA) and sort by CGPA descending
    participants = [(f"Person {i+1}", cgpas[i]) for i in range(num_participants)]
    participants.sort(key=lambda x: -x[1])  # Sort by CGPA descending

    # Initialize empty groups
    groups = [[] for _ in range(num_groups)]

    def group_avg(group):
        if not group:
            return 0
        return sum(x[1] for x in group) / len(group)

    # Greedy assignment: assign each participant to the group with lowest current avg CGPA and < 4 members
    for person in participants:
        # Filter groups with < 4 members
        eligible_groups = [g for g in groups if len(g) < 4]
        # Choose group with lowest average CGPA
        best_group = min(eligible_groups, key=group_avg)
        best_group.append(person)

    # Show results
    st.subheader("📋 Final Groups")
    for i, group in enumerate(groups):
        group_df = pd.DataFrame(group, columns=["Participant", "CGPA"])
        group_df["Group #"] = f"Group {i+1}"
        st.table(group_df[["Group #", "Participant", "CGPA"]])

    # Show group averages
    st.subheader("📊 Group Average CGPAs")
    avg_data = []
    for i, group in enumerate(groups):
        avg = round(group_avg(group), 2)
        avg_data.append((f"Group {i+1}", avg))
    st.table(pd.DataFrame(avg_data, columns=["Group", "Average CGPA"]))
