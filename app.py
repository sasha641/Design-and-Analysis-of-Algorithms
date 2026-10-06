import streamlit as st
import time
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


st.set_page_config(page_title="DAA Algorithm Simulator", layout="wide")


st.markdown("""
<style>
    .stack-element {
        background-color: #4CAF50; color: white; padding: 15px; 
        margin: 5px auto; text-align: center; border-radius: 5px; 
        width: 200px; font-weight: bold; font-size: 18px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .stack-container {
        border-left: 4px solid #333; border-right: 4px solid #333; 
        border-bottom: 4px solid #333; padding: 10px; width: 240px; 
        margin: 0 auto; min-height: 300px; display: flex; 
        flex-direction: column-reverse;
    }
</style>
""", unsafe_allow_html=True)


st.sidebar.title("DAA Simulator")
st.sidebar.markdown("Navigate through the algorithms using the options below:")
option = st.sidebar.radio("Select Topic", [
                          "Stack (Data Structure)", "Binary Search", "Kruskal's Algorithm"])


# ==========================================
# 1. STACK SIMULATOR
# ==========================================
if option == "Stack (Data Structure)":
    st.title("Stack Simulator (LIFO)")
    st.markdown("Demonstrates the **Push**, **Pop**, and **Peek** operations.")

    if 'stack' not in st.session_state:
        st.session_state.stack = []

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.subheader("Controls")
        val = st.text_input("Enter a value to Push:")
        if st.button("Push"):
            if val:
                st.session_state.stack.append(val)
            else:
                st.warning("Please enter a value!")

        if st.button("Pop"):
            if len(st.session_state.stack) > 0:
                popped = st.session_state.stack.pop()
                st.success(f"Popped element: {popped}")
            else:
                st.error("Stack Underflow! Stack is empty.")

        if st.button("Peek"):
            if len(st.session_state.stack) > 0:
                st.info(f"Top element is: {st.session_state.stack[-1]}")
            else:
                st.warning("Stack is empty.")

        if st.button("Clear Stack"):
            st.session_state.stack = []

    with col2:
        st.subheader("Visualization")

        st.write("**Top of Stack**")
        stack_html = "<div class='stack-container'>"
        for item in st.session_state.stack:
            stack_html += f"<div class='stack-element'>{item}</div>"
        stack_html += "</div>"
        st.markdown(stack_html, unsafe_allow_html=True)
        st.write("**Bottom of Stack**")

    with col3:
        st.subheader("Complexity & Details")
        st.info("""
        **Time Complexity:**
        - Push: O(1)
        - Pop: O(1)
        - Peek: O(1)
        
        **Space Complexity:**
        - O(N) where N is the number of elements in the stack.
        
        **Concept:**
        Stack follows the Last-In-First-Out (LIFO) principle. The element inserted last is the first one to be removed.
        """)


# ==========================================
# 2. BINARY SEARCH SIMULATOR
# ==========================================
elif option == "Binary Search":
    st.title("Binary Search Simulator")
    st.markdown(
        "An efficient array search algorithm. Works on **sorted arrays** using a divide and conquer approach.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("User Input")
        arr_input = st.text_input(
            "Enter comma-separated integers:", "2, 5, 8, 12, 16, 23, 38, 56, 72, 91")
        target_input = st.number_input(
            "Target Value to Search:", value=23, step=1)
        start_btn = st.button("Start Simulation")

        st.markdown("---")
        st.subheader("Complexity")
        st.info("""
        **Time Complexity:**
        - Best Case: O(1) (Found at middle)
        - Average / Worst Case: O(log N)
        
        **Space Complexity:**
        - O(1) (Iterative approach)
        """)

    with col2:
        st.subheader("Live Simulation Stages")
        visual_placeholder = st.empty()
        log_placeholder = st.empty()

        if start_btn:
            try:

                arr = [int(x.strip()) for x in arr_input.split(',')]
                arr.sort()
                target = int(target_input)

                low = 0
                high = len(arr) - 1
                found = False

                logs = [
                    f"**Initial Sorted Array:** {arr}", "Starting Search..."]

                def draw_array(arr, l, h, m, is_found=False):
                    html = ""
                    for i, val in enumerate(arr):
                        color = "#e0e0e0"  # Eliminated
                        font_color = "black"
                        if i == m:
                            color = "#4CAF50" if is_found else "#FF9800"  # Green if found, Orange if mid
                            font_color = "white"
                        elif l <= i <= h:
                            color = "#2196F3"  # Blue for active search space
                            font_color = "white"

                        html += f"<div style='display:inline-block; margin:5px; padding:15px 20px; background-color:{color}; color:{font_color}; font-weight:bold; border-radius:5px; font-size:18px;'>{val}</div>"
                    return html

                step = 1
                while low <= high:
                    mid = (low + high) // 2

                    visual_placeholder.markdown(draw_array(
                        arr, low, high, mid), unsafe_allow_html=True)
                    logs.append(
                        f"**Step {step}:** Low={low}, High={high}, Mid={mid} (Value: {arr[mid]})")
                    log_placeholder.markdown(
                        "<br>".join(logs), unsafe_allow_html=True)
                    time.sleep(1.5)  # Pause for animation

                    if arr[mid] == target:
                        visual_placeholder.markdown(draw_array(
                            arr, low, high, mid, True), unsafe_allow_html=True)
                        logs.append(
                            f"✅ **Target {target} found at index {mid}!**")
                        log_placeholder.markdown(
                            "<br>".join(logs), unsafe_allow_html=True)
                        found = True
                        break
                    elif arr[mid] < target:
                        logs.append(
                            f"↳ {arr[mid]} < {target}. Discarding left half.")
                        low = mid + 1
                    else:
                        logs.append(
                            f"↳ {arr[mid]} > {target}. Discarding right half.")
                        high = mid - 1

                    step += 1
                    time.sleep(1)

                if not found:
                    visual_placeholder.markdown(draw_array(
                        arr, -1, -1, -1), unsafe_allow_html=True)
                    logs.append(
                        f"❌ **Target {target} not found in the array.**")
                    log_placeholder.markdown(
                        "<br>".join(logs), unsafe_allow_html=True)

            except ValueError:
                st.error("Please enter valid integers separated by commas.")


# ==========================================
# 3. KRUSKAL'S ALGORITHM SIMULATOR
# ==========================================
elif option == "Kruskal's Algorithm":
    st.title("Kruskal's Algorithm (Minimum Spanning Tree)")
    st.markdown(
        "Finds the Minimum Spanning Tree (MST) of a graph using the greedy approach and a Disjoint Set (Union-Find).")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Graph Edges Input")
        st.write("Edit the table below to add/remove edges.")

        if 'graph_data' not in st.session_state:
            st.session_state.graph_data = pd.DataFrame({
                'Source': ['A', 'A', 'A', 'B', 'C', 'C'],
                'Target': ['B', 'C', 'D', 'D', 'D', 'B'],
                'Weight': [10, 6, 5, 15, 4, 3]
            })

        df = st.data_editor(st.session_state.graph_data,
                            num_rows="dynamic", use_container_width=True)
        run_kruskal = st.button("Run Kruskal's Simulation")

        st.markdown("---")
        st.subheader("Complexity")
        st.info("""
        **Time Complexity:** 
        - O(E log E) or O(E log V) (Sorting edges dictates the time)
        
        **Space Complexity:** 
        - O(V + E) for storing the graph and Union-Find arrays.
        """)

    with col2:
        st.subheader("Step-by-Step Visualization")
        if run_kruskal:

            class DisjointSet:
                def __init__(self, vertices):
                    self.parent = {v: v for v in vertices}
                    self.rank = {v: 0 for v in vertices}

                def find(self, item):
                    if self.parent[item] == item:
                        return item
                    self.parent[item] = self.find(self.parent[item])
                    return self.parent[item]

                def union(self, x, y):
                    xroot = self.find(x)
                    yroot = self.find(y)
                    if self.rank[xroot] < self.rank[yroot]:
                        self.parent[xroot] = yroot
                    elif self.rank[xroot] > self.rank[yroot]:
                        self.parent[yroot] = xroot
                    else:
                        self.parent[yroot] = xroot
                        self.rank[xroot] += 1

            edges = []
            vertices = set()
            for _, row in df.iterrows():
                u, v, w = str(row['Source']).strip(), str(
                    row['Target']).strip(), float(row['Weight'])
                edges.append((u, v, w))
                vertices.add(u)
                vertices.add(v)

            G = nx.Graph()
            for u, v, w in edges:
                G.add_edge(u, v, weight=w)

            pos = nx.spring_layout(G, seed=42)

            def draw_graph(mst_edges, current_edge=None, cycle_edge=None):
                fig, ax = plt.subplots(figsize=(6, 4))

                nx.draw_networkx_nodes(
                    G, pos, node_color='lightblue', node_size=500, ax=ax)
                nx.draw_networkx_labels(
                    G, pos, font_size=12, font_weight="bold", ax=ax)
                nx.draw_networkx_edges(
                    G, pos, edge_color='#e0e0e0', width=1.5, ax=ax)

                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(
                    G, pos, edge_labels=edge_labels, ax=ax)

                if mst_edges:
                    nx.draw_networkx_edges(G, pos, edgelist=[(
                        u, v) for u, v, _ in mst_edges], edge_color='green', width=3.5, ax=ax)

                if current_edge:
                    nx.draw_networkx_edges(G, pos, edgelist=[(
                        current_edge[0], current_edge[1])], edge_color='orange', width=3.5, ax=ax)

                if cycle_edge:
                    nx.draw_networkx_edges(G, pos, edgelist=[(
                        cycle_edge[0], cycle_edge[1])], edge_color='red', width=3.5, ax=ax)

                plt.axis('off')
                return fig

            edges = sorted(edges, key=lambda item: item[2])  # Sort by weight
            ds = DisjointSet(vertices)
            mst = []
            total_cost = 0

            st.markdown("**1. Edges Sorted by Weight:**")
            st.write([f"{u}-{v} ({w})" for u, v, w in edges])

            graph_placeholder = st.empty()
            info_placeholder = st.empty()

            graph_placeholder.pyplot(draw_graph([]))
            time.sleep(1.5)

            step = 1
            for u, v, w in edges:
                info_placeholder.markdown(
                    f"**Step {step}:** Evaluating edge **{u}-{v}** (Weight: {w})")
                graph_placeholder.pyplot(
                    draw_graph(mst, current_edge=(u, v, w)))
                time.sleep(1.5)

                x = ds.find(u)
                y = ds.find(v)

                if x != y:  # No cycle
                    ds.union(x, y)
                    mst.append((u, v, w))
                    total_cost += w
                    info_placeholder.markdown(
                        f"**Step {step}:** ✅ Edge **{u}-{v}** added to MST. No cycle formed.")
                else:  # Cycle
                    graph_placeholder.pyplot(
                        draw_graph(mst, cycle_edge=(u, v, w)))
                    info_placeholder.markdown(
                        f"**Step {step}:** ❌ Edge **{u}-{v}** creates a cycle! Discarding.")
                    time.sleep(1.5)

                graph_placeholder.pyplot(draw_graph(mst))
                step += 1
                time.sleep(1)

            st.success(
                f"**Algorithm Complete! Minimum Spanning Tree Cost = {total_cost}**")
            st.write("**Final MST Edges:**", [f"{u}-{v}" for u, v, w in mst])
