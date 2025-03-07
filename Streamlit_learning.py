# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# st.title("User Input in Streamlit")

# # Create a text input
# user_input_name = st.text_input("Enter your name:")
# user_input_surname = st.text_input("Enter your surname :")

# # Button to submit
   
# # Slider for selecting a number
# age = st.slider("Select your age", 1, 100, 25)
# st.write(f"Your selected age: {age}")

# # Checkbox for Yes/No selection
# agree = st.checkbox("I agree to the terms and conditions")
# if agree:
#     st.write("Thank you for agreeing!")

# # Radio buttons for choices
# color = st.radio("Pick a color:", ["Red", "Green", "Blue"])
# st.write(f"You selected: {color}")

# if st.button("Submit"):
#     st.write(f"Hello, {user_input_name}!"+f" {user_input_surname}")



# st.title("Upload an Excel File and Convert to DataFrame")

# # File uploader for Excel files
# uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# if uploaded_file is not None:
#     # Read the Excel file
#     df = pd.read_excel(uploaded_file)

#     # Display the DataFrame
#     st.write("### Data Preview:")
#     st.dataframe(df)

#     # # Show basic statistics
#     # st.write("### Summary Statistics:")
#     # st.write(df.describe())

#         # Select a column to visualize
#     column = st.selectbox("Select a column to visualize", df.columns)

#     # Plot the selected column
#     fig, ax = plt.subplots()
#     ax.hist(df[column].dropna(), bins=20, edgecolor="black")
#     ax.set_title(f"Histogram of {column}")
#     ax.set_xlabel(column)
#     ax.set_ylabel("Frequency")

#     # Display the plot in Streamlit
#     st.pyplot(fig)



# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# st.title("Upload Excel File and Plot Multi-Line Chart")

# # File uploader
# uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"],key="1")

# if uploaded_file is not None:
#     # Read the Excel file
#     df = pd.read_excel(uploaded_file)

#     # Display the DataFrame
#     st.write("### Data Preview:")
#     st.dataframe(df)

#     # Select X-axis column
#     x_axis = st.selectbox("Select X-axis", df.columns)

#     # Select multiple Y-axis columns
#     y_axes = st.multiselect("Select Y-axis (Multiple Allowed)", df.columns)
    
#     # Plot only if at least one Y-axis column is selected
#     if y_axes:
#         fig, ax = plt.subplots()

#         for y in y_axes:
#             # ax.plot(df[x_axis], df[y], marker="o", linestyle="-", label=y)
#             # ax.fill_between(df[x_axis], df[y], alpha=0.4)
#             ax.bar(df[x_axis], df[y])

#         ax.set_xlabel(x_axis)
#         ax.set_ylabel("Values")
#         ax.set_title(f"Multi-Line Chart of {', '.join(y_axes)} vs {x_axis}")
#         ax.legend()  # Show legend

#         # Display the plot
#         st.pyplot(fig)

   

#     st.title("Upload Excel File and Apply Heatmap to Multiple Columns")

#     # File uploader
#     uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"],key="2")

#     if uploaded_file is not None:
#         # Read the Excel file
#         df = pd.read_excel(uploaded_file)

#         # Display the DataFrame
#         st.write("### Data Preview:")
#         st.dataframe(df)

#         # Select numerical columns
#         numeric_cols = df.select_dtypes(include=["number"]).columns

#         if len(numeric_cols) == 0:
#             st.warning("No numerical columns found.")
#         else:
#             # Allow multiple column selection
#             selected_cols = st.multiselect("Select columns to apply heatmap", numeric_cols)

#             if selected_cols:
#                 # Apply background gradient to multiple selected columns at once
#                 styled_df = df.style.background_gradient(subset=selected_cols, cmap="coolwarm")

#                 # Display the styled DataFrame
#                 st.write("### Heatmap Applied to Selected Columns:")
#                 st.dataframe(styled_df)


# import streamlit as st
# import pandas as pd

# st.title("Streamlit Sidebar Example")

# # Sidebar for file upload
# uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
    
#     # Sidebar for column selection
#     numeric_cols = df.select_dtypes(include=["number"]).columns
#     selected_col = st.sidebar.selectbox("Select a column", numeric_cols)

#     st.write("### Data Preview:")
#     st.dataframe(df)



import streamlit as st
import pandas as pd

st.title("Streamlit Layout Example")

# Create columns for side-by-side layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

with col2:
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        selected_col = st.selectbox("Select a column", numeric_cols)

if uploaded_file:
    st.write("### Data Preview:")
    st.dataframe(df)
