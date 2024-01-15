import streamlit as st
import pandas as pd
import pydeck as pdk
import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation

df = pd.read_csv("https://raw.githubusercontent.com/Kten987/streamlit/ea2519c94a15fb22d557baba8b2576538270cfde/streamlit/total_gg_hcm.csv")
df.drop(['address_ward', 'address_street', 'address_city', 'address_postal_code', 'address_state', 'address_country_code'], axis=1, inplace=True)

# Display the login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

# Check if the username and password are correct
if username == "kten987" and password == "123":
    logged_in = True
else:
    logged_in = False
    st.write("<span style='color:red'>Sai thông tin đăng nhập!</span>", unsafe_allow_html=True)

# Display the dataframe and other content only if the user is logged in
if logged_in:
    st.header("KV MAP")

    # Filter the dataframe based on user selection
    city_options = np.append("All", df['City'].unique())
    city = st.selectbox("Chọn thành phố", city_options, index=0)
    if city != "All":
        df = df[df['City'] == city] 
    else:
        df = df

    district_options = np.append("All", df['District'].unique())
    district = st.selectbox("Chọn quận/huyện", district_options)
    if district != "All":
        df = df[df['District'] == district]
    else:
        df = df

    ward_options = np.append("All", df['Ward'].unique())
    ward = st.selectbox("Chọn phường/xã", ward_options)
    if ward != "All":
        df = df[df['Ward'] == ward]
    else:
        df = df

    cleaned_street_options = np.append("All", df['cleaned_street'].unique())
    cleaned_street = st.selectbox("Chọn đường", cleaned_street_options)
    if cleaned_street != "All":
        df = df[df['cleaned_street'] == cleaned_street]
    else:
        df = df

    name_options = np.append("All", df['name'].unique())
    name_ = st.selectbox("Tên gian hàng", name_options)
    if name_ != "All":
        df = df[df['name'] == name_]
    else:
        df = df

    # search = st.button("Tìm kiếm")

    # if search:
    #     df = df[((df['City'] == city) if city != "All" else True) &  ((df['District'] == district) if district != "All" else True) & 
    #             ((df['Ward'] == ward) if ward != "All" else True) & ((df['cleaned_street'] == cleaned_street) if cleaned_street != "All" else True) & ((df['name'] == name_) if name_ != "All" else True)]


    # st.dataframe(filtered_df)
    # Thêm cột mới vào dataframe
    df['Trạng thái'] = "Chưa tiếp cận"
    df['Đổi thủ'] = None
    st.subheader("Cập nhật trạng thái gian hàng")

    with st.form("Form1"):
        name = st.selectbox("Tên gian hàng", df['name'].unique())
        status = st.selectbox("Trạng thái", ("Đang sử dụng KV", "Đang sử dụng đối thủ", "Gian hàng quá nhỏ", "Gian hàng không tồn tại", "Khác"))
        # if status == "Đang sử dụng đối thủ":
        competitor = st.selectbox("Đối thủ", ("Sapo","Ipos", "POS365", "Misa", "Ocha", "Viettel", "Cukcuk", "Haraven", "VNPT", "Nhanh", "Pancake", "Nobita" , "VNPay", "Ngân long", "Getfly", "Mekong", "Nextsoft", "ABCpay", "EZSpa"))
        submit = st.form_submit_button("Cập nhật")
        if submit:
            df.loc[df["name"] == name, ["Trạng thái", "Đổi thủ"]] = [status, competitor]
            st.success("Đã cập nhật trạng thái thành công!")

    # Hiển thị danh sách gian hàng google với cột mới
    st.header("Danh sách gian hàng google")
    st.write("Số lượng gian hàng: ", len(df["place_id"].unique()))
    st.dataframe(df[['name', 'industry', 'address', 'phone', 'website', 'cleaned_street', 'Ward', 'District', 'City', 'Trạng thái']].drop_duplicates())

    # Hiển thị bản đồ
    # Check if the "lat" and "lng" columns are not empty
    if not df["lat"].empty and not df["lng"].empty:
        # Rename the longitude column to 'lon'
        df.rename(columns={"lng": "lon"}, inplace=True)

        # Create a map centered at the first coordinate in the DataFrame
        center_lat, center_lon = df["lat"].iloc[0], df["lon"].iloc[0]
        view_state = pdk.ViewState(latitude=float(center_lat), longitude=float(center_lon), zoom=12)

        # Create a layer for the markers
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_radius=2,
            get_fill_color=[255, 0, 0],  # Change the color value to a valid format, e.g., [255, 0, 0] for red
            pickable=True,
        )

        # Create the map
        map = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer],
        )

        # Display the map
        st.header("Bản đồ")
        st.pydeck_chart(map)

        # # Display the markers as red dots
        # st.map(df, zoom=12, color="#FF0000")  # Change the color value to a valid format, e.g., "red" to [255, 0, 0]
    else:
        st.write("No coordinates found in the DataFrame.")




