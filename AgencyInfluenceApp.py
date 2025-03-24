import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decimal import Decimal
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from streamlit_elements import elements


#data = pd.read_csv(f"G:\My Drive\Analytics team\Streamlit\AgencyInfluence\ClubAgencyInfluence.csv")
data = pd.read_csv("ClubAgencyInfluence.csv")

data_show = data[['Competition','squad','agency','PlayerPercentage','PlayerValuePercentage','HeadCoach','TotalDeals','DealsValuePercentage','InfluenceIndex']]

data_show.rename(columns={'squad':'Squad','agency':'Agency'}, inplace=True)


st.set_page_config(
     page_title="TransferRoom Agency Influence Index",
     #page_icon="🧊",
     layout="wide",
     #initial_sidebar_state="expanded",
 )



st.markdown("<font color=darkblue>Transfer</font><font color=green>Room</font>", unsafe_allow_html=True)
st.title("Agency Influence Index")


percentage_columns = ['PlayerPercentage', 'PlayerValuePercentage', 'DealsValuePercentage']
data_show[percentage_columns] = data_show[percentage_columns]*100
data_show[percentage_columns] = data_show[percentage_columns].applymap(lambda x: f'{x:.1f}%')


data_show['InfluenceIndex'] = data_show['InfluenceIndex'].astype(int)  #data_show.InfluenceIndex.round(decimals=1)




# Sidebar layout for filters
col1, col2, col3 = st.columns(3)

with col1:
    competition_filter = st.multiselect("Filter by Competition", options=sorted(data_show['Competition'].unique()))

# Filter data based on Competition selection
filtered_data = data_show.copy()
if competition_filter:
    filtered_data = filtered_data[filtered_data['Competition'].isin(competition_filter)]

with col2:
    squad_filter = st.multiselect("Filter by Squad", options=sorted(filtered_data['Squad'].unique()))

# Filter data based on Squad selection
if squad_filter:
    filtered_data = filtered_data[filtered_data['Squad'].isin(squad_filter)]

with col3:
    agency_filter = st.multiselect("Filter by Agency", options=sorted(filtered_data['Agency'].unique()))

# Filter data based on Agency selection
if agency_filter:
    filtered_data = filtered_data[filtered_data['Agency'].isin(agency_filter)]


filtered_data = filtered_data.sort_values(by=['InfluenceIndex'],ascending=False)


# # Displaying table with clickable rows
# clicked_index = st.data_editor(filtered_data, num_rows="dynamic", key="editable_table")

# # Check if a row is clicked
# if clicked_index is not None:
#     clicked_row = filtered_data.iloc[clicked_index]
#     with st.sidebar:
#         st.write("### Row Details")
#         st.write(f"**Squad:** {clicked_row['Squad']}")
#         st.write(f"**Agency:** {clicked_row['Agency']}")

# Define a red-to-green colormap
cmap = LinearSegmentedColormap.from_list('red_green', ['#dfe2e8', '#0e9655'])
filtered_data = filtered_data.style.bar(subset=['InfluenceIndex'],cmap=cmap,align='left', vmin=10, height=50,width=90)





# Define custom CSS for styling the table
table_style = '''
    <style>

    /* Hide the table row index */
    tbody th {
        display: none;
    }
    .blank {
        display: none;
    }
    </style>
'''

# Apply the style before displaying the table
st.markdown(table_style, unsafe_allow_html=True)


st.table(filtered_data)
