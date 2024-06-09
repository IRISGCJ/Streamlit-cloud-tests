import geopandas as gpd
import streamlit as st

#用绝对路径读取道路数据和省份数据
provinces_path = r'c:\data\china\china_provinces.shp'
roads_path = r'c:\data\china\china_roads.shp'

provinces_gdf = gpd.read_file(provinces_path)
roads_gdf = gpd.read_file(roads_path)


st.title("查询省级行政单元的信息") #标题

# 创建表单封装
with st.form("province_form"):
    # 下拉单选框
    province_names = provinces_gdf['NAME'].tolist()
    selected_province = st.selectbox('选择一个省级行政单元', province_names)
    
    # 复选框
    include_overlaps = st.checkbox('相邻省份包含overlaps关系')
    
    # 表单提交按钮
    submit_button = st.form_submit_button(label='查询')

# 表单提交后执行的操作
if submit_button:
    # 获取选中省的几何对象
    selected_province_geom = provinces_gdf[provinces_gdf['NAME'] == selected_province].geometry.iloc[0]

    # 计算面积str
    area_sq_km = selected_province_geom.area / 1e6  # 米转平方公里
    st.write(f"面积: {area_sq_km:.2f} 平方公里")
    
    # 道路数据与省级行政单元进行空间叠置
    roads_in_province = gpd.overlay(roads_gdf, provinces_gdf[provinces_gdf['NAME'] == selected_province], how='intersection')
    

    total_road_length_km = roads_in_province.length.sum() / 1e3  # 米转公里
    road_density_km_per_sq_km = total_road_length_km / area_sq_km
    st.write(f"道路总长度: {total_road_length_km:.2f} 公里")
    st.write(f"道路密度: {road_density_km_per_sq_km:.4f} 公里/平方公里")
    
    # 查询相邻省份
    neighbors = provinces_gdf[provinces_gdf.touches(selected_province_geom)]
    
    #判断是否overlaps
    if include_overlaps:
        neighbors = provinces_gdf[provinces_gdf.overlaps(selected_province_geom) | provinces_gdf.touches(selected_province_geom)]
    neighbor_names = neighbors['NAME'].tolist()
    
    st.write(f"相邻省份数量: {len(neighbor_names)}")
    st.write("相邻省份名称: " + ", ".join(neighbor_names))
