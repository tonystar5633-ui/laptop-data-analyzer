import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------------------------------------
# 0. Configuration and Helper Functions
# -----------------------------------------------------------
st.set_page_config(layout="wide", page_title="Advanced Laptop Data Analyzer")

@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a CSV string for download."""
    return df.to_csv().encode('utf-8')

def lakh_to_inr(lakhs):
    """Converts a value in Lakhs (Lakh) to Indian Rupees (INR)."""
    if isinstance(lakhs, str):
        if 'Lakh' in lakhs:
            value = float(lakhs.replace('₹', '').replace(' Lakh', '').replace(',', ''))
            return int(value * 100000)
        elif 'L' in lakhs:
            value = float(lakhs.replace('₹', '').replace(' L', '').replace(',', ''))
            return int(value * 100000)
        elif 'Crore' in lakhs:
            value = float(lakhs.replace('₹', '').replace(' Crore', '').replace(',', ''))
            return int(value * 10000000)
        elif ' Lakh' in lakhs:
            value = float(lakhs.replace('₹', '').replace(' Lakh', '').replace(',', ''))
            return int(value * 100000)
        else:
            return int(lakhs.replace('₹', '').replace(',', '').replace(' ', ''))
    return int(lakhs)

# -----------------------------------------------------------
# 1. Data Structure 
# (Re-using the detailed data from the previous script)
# -----------------------------------------------------------
# Sample laptop data using real INR prices and detailed specifications
LAPTOP_DATA_INR = [
    {
        "name": "IdeaPad Slim 3", "brand": "Lenovo", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "13th Gen Core i7 13620H", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.28, "spec_score": 55, "price_inr": 65990,
        "gpu_type": "Integrated Intel UHD Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Vivobook 14", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "Intel Core Ultra 7 255H", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 14.0, "spec_score": 68, "price_inr": 79990,
        "gpu_type": "Intel Integrated Intel", "gpu_vram_gb": 0,
    },
    {
        "name": "MateBook Fold", "brand": "Huawei", "os": "HarmonyOS 5", "utility": "Business",
        "cpu_full": "Kirin X90", "ram_gb": 32, "storage_gb": 2048, 
        "screen_size_in": 18.0, "spec_score": 61, "price_inr": 319930,
        "gpu_type": "Integrated", "gpu_vram_gb": 0,
    },
    {
        "name": "Nitro V 16", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "14th Gen Core i5 14450HX", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 16.0, "spec_score": 68, "price_inr": 84990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Aspire Lite AL15", "brand": "Acer", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Core i5 12450H", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 56, "price_inr": 36541,
        "gpu_type": "Intel UHD Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Victus 15", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 8645HS", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 65990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Thin A15 AI", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 49990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "HP 15s-fq5327TU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Core i3 1215U", "ram_gb": 8, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 55, "price_inr": 37900,
        "gpu_type": "Intel UHD Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Aspire 7 A715", "brand": "Acer", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "13th Gen Core i5 13420H", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 64, "price_inr": 52990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "HP ‎15-fd0467TU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "13th Gen Core i5 1334U", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 57, "price_inr": 49550,
        "gpu_type": "Intel Iris Xe Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Expertbook P1 14", "brand": "Asus", "os": "Windows 11", "utility": "Business",
        "cpu_full": "13th Gen Core i3 1315U", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 14.0, "spec_score": 60, "price_inr": 41990,
        "gpu_type": "Intel Integrated UHD", "gpu_vram_gb": 0,
    },
    {
        "name": "MacBook Air 2025", "brand": "Apple", "os": "Mac OS", "utility": "Everyday Use",
        "cpu_full": "Apple M4", "ram_gb": 16, "storage_gb": 256, 
        "screen_size_in": 13.6, "spec_score": 45, "price_inr": 95990,
        "gpu_type": "Apple 8 Core GPU", "gpu_vram_gb": 0,
    },
    {
        "name": "Galaxy Book 4", "brand": "Samsung", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "13th Gen Intel Core i3 1315U", "ram_gb": 8, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 54, "price_inr": 37999,
        "gpu_type": "Intel Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "MacBook Air 2022", "brand": "Apple", "os": "Mac OS", "utility": "Everyday Use",
        "cpu_full": "Apple M2", "ram_gb": 16, "storage_gb": 256, 
        "screen_size_in": 13.6, "spec_score": 42, "price_inr": 64990,
        "gpu_type": "10-Core GPU", "gpu_vram_gb": 0,
    },
    {
        "name": "Aspire 3 A324", "brand": "Acer", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Core i3 1215U", "ram_gb": 8, "storage_gb": 512, 
        "screen_size_in": 14.0, "spec_score": 51, "price_inr": 27990,
        "gpu_type": "Intel Integrated UHD", "gpu_vram_gb": 0,
    },
    {
        "name": "Latitude 3550", "brand": "Dell", "os": "Windows 11", "utility": "Business",
        "cpu_full": "13th Gen Core i3 1315U", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 59, "price_inr": 37990,
        "gpu_type": "Intel Integrated UHD Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Victus 15-fa2382TX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "14th Gen Core i5 14450HX", "ram_gb": 24, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 84989,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "LOQ 83JE00U7IN", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "14th Gen Core i7 14700HX", "ram_gb": 16, "storage_gb": 1024, # 1TB SSD
        "screen_size_in": 15.6, "spec_score": 78, "price_inr": 112116,
        "gpu_type": "NVIDIA GeForce RTX 5050", "gpu_vram_gb": 8,
    },
    {
        "name": "TUF Gaming A15", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435HS", "ram_gb": 16, "storage_gb": 1024, # 1TB SSD
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 66990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "LOQ 15ARP9", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435H", "ram_gb": 24, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 93290,
        "gpu_type": "NVIDIA GeForce RTX 4060", "gpu_vram_gb": 8,
    },
    {
        "name": "Zenbook Pro Duo 16", "brand": "Asus", "os": "Windows 11 Pro", "utility": "Creative/Pro",
        "cpu_full": "Intel Core Ultra 9 285H", "ram_gb": 32, "storage_gb": 2048, 
        "screen_size_in": 16.0, "spec_score": 85, "price_inr": 235990,
        "gpu_type": "NVIDIA GeForce RTX 5080", "gpu_vram_gb": 16,
    },
    {
        "name": "Latitude 5400", "brand": "Dell", "os": "Windows 11 Pro", "utility": "Business",
        "cpu_full": "14th Gen Core i5 1430U", "ram_gb": 8, "storage_gb": 256, 
        "screen_size_in": 14.0, "spec_score": 58, "price_inr": 54990,
        "gpu_type": "Intel Integrated Iris Xe", "gpu_vram_gb": 0,
    },
    {
        "name": "OMEN 17", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "14th Gen Core i9 14900HX", "ram_gb": 32, "storage_gb": 1024, 
        "screen_size_in": 17.3, "spec_score": 92, "price_inr": 195000,
        "gpu_type": "NVIDIA GeForce RTX 5090", "gpu_vram_gb": 16,
    },
    {
        "name": "ThinkPad X1 Carbon", "brand": "Lenovo", "os": "Windows 11 Pro", "utility": "Business",
        "cpu_full": "Intel Core Ultra 7 165U", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 14.0, "spec_score": 62, "price_inr": 139990,
        "gpu_type": "Integrated Intel Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "Chromebook Plus", "brand": "Acer", "os": "ChromeOS", "utility": "Everyday Use",
        "cpu_full": "Intel Core i3 N305", "ram_gb": 8, "storage_gb": 256, 
        "screen_size_in": 15.6, "spec_score": 40, "price_inr": 29990,
        "gpu_type": "Integrated Intel UHD", "gpu_vram_gb": 0,
    },
    {
        "name": "Blade 14", "brand": "Razer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 9 8945HS", "ram_gb": 32, "storage_gb": 1024, 
        "screen_size_in": 14.0, "spec_score": 80, "price_inr": 169000,
        "gpu_type": "NVIDIA GeForce RTX 4070", "gpu_vram_gb": 8,
    },
    {
        "name": "Surface Laptop 7", "brand": "Microsoft", "os": "Windows 11 Pro", "utility": "Business",
        "cpu_full": "Snapdragon X Elite", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 13.8, "spec_score": 65, "price_inr": 124999,
        "gpu_type": "Qualcomm Adreno GPU", "gpu_vram_gb": 0,
    },
    {
        "name": "Alienware m18 R3", "brand": "Dell", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "Intel Core i9 15980HX", "ram_gb": 64, "storage_gb": 4096, # 4TB SSD
        "screen_size_in": 18.0, "spec_score": 98, "price_inr": 419999,
        "gpu_type": "NVIDIA GeForce RTX 5090", "gpu_vram_gb": 16,
    },
    {
        "name": "Vivobook S15", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "AMD Ryzen AI 9 HX 370", "ram_gb": 32, "storage_gb": 1024, 
        "screen_size_in": 15.6, "spec_score": 75, "price_inr": 109990,
        "gpu_type": "AMD Radeon 880M", "gpu_vram_gb": 0,
    },
    {
        "name": "ProBook 450 G11", "brand": "HP", "os": "Windows 11 Pro", "utility": "Business",
        "cpu_full": "Intel Core Ultra 5 125U", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 15.6, "spec_score": 60, "price_inr": 89990,
        "gpu_type": "Integrated Intel Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "ThinkBook 16", "brand": "Lenovo", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "Intel Core 5 210H", "ram_gb": 16, "storage_gb": 512, 
        "screen_size_in": 16.0, "spec_score": 52, "price_inr": 59990,
        "gpu_type": "Integrated Intel Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Swift Go 14", "brand": "Acer", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 5 7535U", "ram_gb": 8, "storage_gb": 512, 
        "screen_size_in": 14.0, "spec_score": 48, "price_inr": 45990,
        "gpu_type": "AMD Radeon 660M", "gpu_vram_gb": 0,
    },
    {
        "name": "Zephyrus G14 2025", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen AI 9 HX 370", "ram_gb": 32, "storage_gb": 2048,
        "screen_size_in": 14.0, "spec_score": 88, "price_inr": 221990,
        "gpu_type": "NVIDIA GeForce RTX 5070 Ti", "gpu_vram_gb": 12,
    },
    {
        "name": "Omen 16-xd0015AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7840HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.1, "spec_score": 75, "price_inr": 95989,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Katana A17 AI B8VE-884IN", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 9 8945HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 17.3, "spec_score": 75, "price_inr": 96990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 15-fb2117AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 8845HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 74, "price_inr": 90990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Summit E14 Flip Evo", "brand": "MSI", "os": "Windows 11", "utility": "Business",
        "cpu_full": "13th Gen Intel Core i7 1360P", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 74, "price_inr": 94990,
        "gpu_type": "Intel Integrated Iris Xe", "gpu_vram_gb": 0,
    },
    {
        "name": "TUF Gaming A15 FA507NUR", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 73, "price_inr": 81990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Katana 15 HX B14WEK", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "14th Gen Intel Core i5 14450HX", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 73, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce RTX 5050", "gpu_vram_gb": 8,
    },
    {
        "name": "Yoga 7 14ARP8", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 7735U", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 73, "price_inr": 84890,
        "gpu_type": "Integrated AMD Radeon 680M Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Victus 15-fa1134TX", "brand": "HP", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 73, "price_inr": 79749,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Thin A15 AI B7VE-065IN", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7735HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 73, "price_inr": 93511,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "ROG Zephyrus G15 GA503RM", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 6800HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 73, "price_inr": 99800,
        "gpu_type": "NVIDIA GeForce RTX 3060", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 16-s0095AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7840HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.1, "spec_score": 72, "price_inr": 82450,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 15-fb3012AX (RTX 3050)", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 8645HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 65990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "LOQ 15ARP9 (RTX 4060)", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435H", "ram_gb": 24, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 93290,
        "gpu_type": "NVIDIA GeForce RTX 4060", "gpu_vram_gb": 8,
    },
    {
        "name": "Victus 15-fb3009AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 8645HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 65399,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "TUF Gaming F16 FX608JH", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i5 13450HX", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.0, "spec_score": 72, "price_inr": 99990,
        "gpu_type": "NVIDIA GeForce RTX 5050", "gpu_vram_gb": 8,
    },
    {
        "name": "Creator M16 A11UD", "brand": "MSI", "os": "Windows 10", "utility": "Creative/Pro",
        "cpu_full": "11th Gen Intel Core i7 11800H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.0, "spec_score": 72, "price_inr": 74989,
        "gpu_type": "NVIDIA GeForce RTX 3050 Ti", "gpu_vram_gb": 4,
    },
    {
        "name": "Zenbook 14 OLED 2025", "brand": "Asus", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 5 225H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 72, "price_inr": 92990,
        "gpu_type": "Intel Integrated Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "VenturePro 15 AI A1UDXG", "brand": "MSI", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "Intel Core Ultra 5 125H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 95990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "TUF Gaming F15 FX577ZC (RTX 3050)", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12700H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 72, "price_inr": 79990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "Nitro 16 AN16-41 (8GB RAM)", "brand": "Acer", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7840HS", "ram_gb": 8, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 72, "price_inr": 98349,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Spectre x360 13-ef0053TU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Intel Core i7 1255U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 13.5, "spec_score": 72, "price_inr": 91449,
        "gpu_type": "Intel Iris X Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "TUF Gaming A15 FA566NCR-HN075W (RTX 3050)", "brand": "Asus", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435HS", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 66990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "Victus 15-fa0187TX (RTX 3050)", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 82999,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "ThinkPad E14 Gen 6 (32GB RAM)", "brand": "Lenovo", "os": "Windows 11", "utility": "Business",
        "cpu_full": "Intel Core Ultra 5 125U", "ram_gb": 32, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 71, "price_inr": 98000,
        "gpu_type": "Integrated Intel Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "OmniBook X Flip 14", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 5 226V", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 71, "price_inr": 97197,
        "gpu_type": "Intel Arc Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Thin 15 B12VE", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 84990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Thin A15 AI B7VE-066IN", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 75511,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Acer Nitro 5 AN515-58", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12700H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 71, "price_inr": 95999,
        "gpu_type": "NVIDIA GeForce RTX 3060", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 16-e1060AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 6800H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.1, "spec_score": 71, "price_inr": 76990,
        "gpu_type": "NVIDIA GeForce RTX 3050 Ti", "gpu_vram_gb": 4,
    },
    {
        "name": "Thin A15 AI B7UC-067IN", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 49990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "LOQ 15ARP9 (RTX 3050A)", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435HS", "ram_gb": 24, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 71290,
        "gpu_type": "NVIDIA GeForce RTX 3050 A", "gpu_vram_gb": 4,
    },
    {
        "name": "Nitro V ANV15-41", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7735HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 71990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "LOQ 83JC00MVIN", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 85290,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 15-fb3004AX (RTX 2050)", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 8645HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 61750,
        "gpu_type": "NVIDIA GeForce RTX 2050", "gpu_vram_gb": 4,
    },
    {
        "name": "TUF Gaming F16 FX677VU", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13620H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 70, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "LOQ 15ARP9 (RTX 4050)", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435H", "ram_gb": 24, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Vivobook 16X 2023 K3605ZC", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 70, "price_inr": 64999,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "Katana A15 AI B8VE-418IN", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 8845HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.75, "spec_score": 70, "price_inr": 82990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Galaxy Book 3 Pro NP960XFG", "brand": "Samsung", "os": "Windows 11", "utility": "Business",
        "cpu_full": "13th Gen Intel Core i7 1360P", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.0, "spec_score": 70, "price_inr": 99259,
        "gpu_type": "Intel Iris Xe Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "ThinkPad E14 Gen 6 (Core Ultra 7)", "brand": "Lenovo", "os": "Windows 11", "utility": "Business",
        "cpu_full": "Intel Core Ultra 7 Series 1 155H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 70, "price_inr": 91390,
        "gpu_type": "Integrated Intel Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Thin 15 B12UC-2240IN", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 71990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "ZBook Firefly 14 G11", "brand": "HP", "os": "Windows 11", "utility": "Business",
        "cpu_full": "Intel Core Ultra 7 155U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 70, "price_inr": 90990,
        "gpu_type": "Intel Arc Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "TUF Gaming A15 FA566NCR-HN075W (RTX 3050)", "brand": "Asus", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7435HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 62248,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "Thin 15 B12UCX", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 60999,
        "gpu_type": "NVIDIA GeForce RTX 2050", "gpu_vram_gb": 4,
    },
    {
        "name": "Prestige 16 AI Evo B1MG", "brand": "MSI", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "Intel Core Ultra 7 Series 1 155H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.0, "spec_score": 70, "price_inr": 88700,
        "gpu_type": "Intel Integrated Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "Vivobook 16X K3605ZF", "brand": "Asus", "os": "Windows 11 Home", "utility": "Performance",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 70, "price_inr": 64999,
        "gpu_type": "NVIDIA GeForce RTX 2050", "gpu_vram_gb": 4,
    },
    {
        "name": "Zbook Power G4-A", "brand": "HP", "os": "Windows 11", "utility": "Business",
        "cpu_full": "AMD Ryzen 7 6800H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 99999,
        "gpu_type": "NVIDIA Quadro T600", "gpu_vram_gb": 4,
    },
    {
        "name": "Envy x360 15-ew0047TU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Intel Core i7 1255U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 88999,
        "gpu_type": "Intel Iris X Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "TUF Gaming F17 FX777ZC", "brand": "Asus", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 17.3, "spec_score": 70, "price_inr": 95899,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "TUF Gaming A17 FA706IU-HX415T", "brand": "Asus", "os": "Windows 10", "utility": "Gaming",
        "cpu_full": "4th Gen AMD Ryzen 7 4800H", "ram_gb": 16, "storage_gb": 256, 
        "screen_size_in": 17.3, "spec_score": 70, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce GTX 1660 Ti", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 15-fa0188TX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 70, "price_inr": 77900,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "LOQ 15IRX9", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i5 13450HX", "ram_gb": 24, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 74787,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "TUF Gaming A15 FA506NCG-HN200WS", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7445HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 65990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "Nitro V ANV15-52", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13620H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce RTX 5050", "gpu_vram_gb": 8,
    },
    {
        "name": "ThinkBook 16 G6", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 7730U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 69, "price_inr": 55550,
        "gpu_type": "AMD Radeon Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Vivobook 16X K3605ZF (RTX 2050)", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 69, "price_inr": 57990,
        "gpu_type": "NVIDIA GeForce RTX 2050", "gpu_vram_gb": 4,
    },
    {
        "name": "Dell G15-5530 (i7, RTX 3050 6GB)", "brand": "Dell", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13650HX", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 90990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Modern 15 H AI C2HMG", "brand": "MSI", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 7 255H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 80990,
        "gpu_type": "Intel Arc Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Vivobook 16X K3605ZU", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 69, "price_inr": 78500,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Yoga 7 14IRL8", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "13th Gen Intel Core i5 1340P", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 85990,
        "gpu_type": "Integrated Intel Iris Xe Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "TUF Gaming F15 FX577ZC-HN193W", "brand": "Asus", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12700H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 82990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "TUF Gaming A15 FA506NC-HN083WS", "brand": "Asus", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 65500,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4,
    },
    {
        "name": "TUF Gaming F15 FX507VU", "brand": "Asus", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13620H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 92990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Nitro V ANV15-51 (1TB SSD)", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13620H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 88750,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Pavilion Plus 16-ab0015TX", "brand": "HP", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "13th Gen Intel Core i5 13500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 69, "price_inr": 82990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Prestige 14 AI Evo C1MG", "brand": "MSI", "os": "Windows 11 Home", "utility": "Business",
        "cpu_full": "Intel Core Ultra 7 155H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 89990,
        "gpu_type": "Intel Integrated Intel Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "Cyborg 15 A12UDX", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i5 12450H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 71699,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Thin A15 AI B7UCX-068IN", "brand": "MSI", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 50800,
        "gpu_type": "NVIDIA GeForce RTX 2050", "gpu_vram_gb": 4,
    },
    {
        "name": "Pavilion Plus 14-ey0789AU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 7840H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 76740,
        "gpu_type": "AMD Radeon 780M Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "LOQ 15APH8 82XT004HIN", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 7 7840HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 83990,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Thin GF63 12VE", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 93499,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Galaxy Book 3 360", "brand": "Samsung", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "13th Gen Intel Core i7 1360P", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 98399,
        "gpu_type": "Intel Iris Xe Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Pavilion Plus 14-eh0037TU", "brand": "HP", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 84699,
        "gpu_type": "Intel Integrated Iris Xe", "gpu_vram_gb": 0,
    },
    {
        "name": "IdeaPad Flex 5 82R90068IN", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 5700U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 67949,
        "gpu_type": "AMD Radeon", "gpu_vram_gb": 0,
    },
    {
        "name": "Omen 16-B0352TX", "brand": "HP", "os": "Windows 10", "utility": "Gaming",
        "cpu_full": "11th Gen Intel Core i7 11800H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 16.1, "spec_score": 69, "price_inr": 99999,
        "gpu_type": "NVIDIA GeForce RTX 3050 Ti Graphics", "gpu_vram_gb": 4,
    },
    {
        "name": "ThinkPad E14 Gen 6 (Core Ultra 7, 1TB)", "brand": "Lenovo", "os": "Windows 11", "utility": "Business",
        "cpu_full": "Intel Core Ultra 7 Series 1 155H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 99950,
        "gpu_type": "Integrated Intel Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Katana 15 B13VEK", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i7 13700H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 95511,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "ThinkPad E14 21JRS0H300", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 7730U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 63850,
        "gpu_type": "AMD Radeon Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Victus 15-FA1402TX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 80100,
        "gpu_type": "NVIDIA GeForce RTX 3050A", "gpu_vram_gb": 4,
    },
    {
        "name": "IdeaPad Flex 5 82R900D9IN", "brand": "Lenovo", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 5700U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 61990,
        "gpu_type": "AMD Radeon", "gpu_vram_gb": 0,
    },
    {
        "name": "Thinkpad E14 G4 21E3S02M00", "brand": "Lenovo", "os": "Windows 11 Pro", "utility": "Business",
        "cpu_full": "12th Gen Intel Core i7 1255U", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 69, "price_inr": 93854,
        "gpu_type": "Intel Iris Xe Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "Katana 15 B12UDXK", "brand": "MSI", "os": "Windows 11 Home", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i7 12650H", "ram_gb": 8, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 69, "price_inr": 90299,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "TUF Gaming A17 FA706IU-H7220T", "brand": "Asus", "os": "Windows 10 Home", "utility": "Gaming",
        "cpu_full": "4th Gen AMD Ryzen 7 4800H", "ram_gb": 16, "storage_gb": 256, 
        "screen_size_in": 17.3, "spec_score": 69, "price_inr": 91099,
        "gpu_type": "NVIDIA Geforce GTX 1660 Ti", "gpu_vram_gb": 6,
    },
    {
        "name": "Vivobook 14 S3407CA (Core Ultra 7)", "brand": "Asus", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 7 255H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 68, "price_inr": 79990,
        "gpu_type": "Intel Integrated Intel", "gpu_vram_gb": 0,
    },
    {
        "name": "Nitro V 16 ANV16-71", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "14th Gen Intel Core i5 14450HX", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 68, "price_inr": 84990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Victus 15-fb0185AX", "brand": "HP", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 5600H", "ram_gb": 8, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 49990,
        "gpu_type": "AMD Radeon RX 6500M", "gpu_vram_gb": 4,
    },
    {
        "name": "Nitro V ANV15-41 UN.QPFSI", "brand": "Acer", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "AMD Ryzen 5 7535HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 63499,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "ThinkBook 16 21MWA0R4IN", "brand": "Lenovo", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "AMD Ryzen 7 7735HS", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 68, "price_inr": 52990,
        "gpu_type": "AMD Radeon Graphics", "gpu_vram_gb": 0,
    },
    {
        "name": "LOQ 83DV007GIN", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i5 13450HX", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 87990,
        "gpu_type": "NVIDIA GeForce RTX 4050", "gpu_vram_gb": 6,
    },
    {
        "name": "Infinix Zerobook 2023", "brand": "Infinix", "os": "Windows 11 Home", "utility": "Everyday Use",
        "cpu_full": "13th Gen Intel Core i9 13900H", "ram_gb": 32, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 87990,
        "gpu_type": "Intel Integrated Iris Xe", "gpu_vram_gb": 0,
    },
    {
        "name": "Dell 15 G15-5530 (i5, 1TB SSD)", "brand": "Dell", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "13th Gen Intel Core i5 13450HX", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 77490,
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 6,
    },
    {
        "name": "Vivobook 14 2025 S3407CA (Core Ultra 5)", "brand": "Asus", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 5 225H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 14.0, "spec_score": 68, "price_inr": 69990,
        "gpu_type": "Intel Integrated UHD", "gpu_vram_gb": 0,
    },
    {
        "name": "LOQ 15IRH8 82XV00F7IN", "brand": "Lenovo", "os": "Windows 11", "utility": "Gaming",
        "cpu_full": "12th Gen Intel Core i5 12450H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 15.6, "spec_score": 68, "price_inr": 82990,
        "gpu_type": "NVIDIA GeForce RTX 4060", "gpu_vram_gb": 8,
    },
    {
        "name": "IdeaPad 5 2-in-1 14IAL10", "brand": "Lenovo", "os": "Windows 11", "utility": "Everyday Use",
        "cpu_full": "Intel Core Ultra 5 225H", "ram_gb": 16, "storage_gb": 1024,
        "screen_size_in": 14.0, "spec_score": 68, "price_inr": 91100,
        "gpu_type": "Intel Integrated Arc", "gpu_vram_gb": 0,
    },
    {
        "name": "Vivobook 16X K3605ZC-RP587WS", "brand": "Asus", "os": "Windows 11", "utility": "Performance",
        "cpu_full": "12th Gen Intel Core i5 12500H", "ram_gb": 16, "storage_gb": 512,
        "screen_size_in": 16.0, "spec_score": 69, "price_inr": 62990, 
        "gpu_type": "NVIDIA GeForce RTX 3050", "gpu_vram_gb": 4, 
    },
]

# Create DataFrame
df = pd.DataFrame(LAPTOP_DATA_INR)

# Clean up column names and set index
df.columns = [
    "Name", "Brand", "OS", "Utility", "CPU Full Model", "RAM (GB)", 
    "Storage (GB)", "Screen (in)", "Spec Score", "Price (Rs)", 
    "GPU Type", "GPU VRAM (GB)"
]

# Reorder columns for display
df = df[[
    "Name", "Brand", "OS", "Utility", "Price (Rs)", "Spec Score", 
    "CPU Full Model", "RAM (GB)", "Storage (GB)", "GPU Type", 
    "GPU VRAM (GB)", "Screen (in)", 
]]
df = df.set_index('Name')

# Extract CPU Brand and Model for filtering
df['CPU Brand'] = df['CPU Full Model'].apply(lambda x: 'Apple' if 'Apple' in x else ('AMD' if 'AMD' in x else ('Intel' if 'Intel' in x or 'Core' in x else 'Other')))
df['Intel CPU Model'] = df['CPU Full Model'].apply(lambda x: next((m for m in ['i9', 'i7', 'i5', 'i3', 'Ultra 9', 'Ultra 7', 'Ultra 5'] if m in x), 'Other') if 'Intel' in x or 'Core' in x else 'N/A')
df['AMD CPU Model'] = df['CPU Full Model'].apply(lambda x: next((m for m in ['Ryzen 9', 'Ryzen 7', 'Ryzen 5', 'Ryzen 3'] if m in x), 'Other') if 'AMD' in x else 'N/A')
df['GPU Dedicated'] = df['GPU VRAM (GB)'].apply(lambda x: 'Dedicated' if x > 0 else 'Integrated')


# -----------------------------------------------------------
# 2. Main Streamlit Application and UI
# -----------------------------------------------------------

def main():
    st.title("💻 Advanced Laptop Data Analyzer & Comparison")
    st.markdown("Use the filters in the sidebar to refine your search and visualize the data.")
    
    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("⚙️ Filter Options")
        
        # 1. Price Range (Using your defined range options)
        st.subheader("💰 Price Filter")
        price_options = {
            'Min': ['₹20,000', '₹25,000', '₹30,000', '₹40,000', '₹50,000', '₹60,000', '₹75,000', '₹1 Lakh', '₹1.25 Lakh', '₹1.5 Lakh', '₹1.75 Lakh', '₹2 Lakh'],
            'Max': ['₹25,000', '₹30,000', '₹40,000', '₹50,000', '₹60,000', '₹75,000', '₹1 Lakh', '₹1.25 Lakh', '₹1.5 Lakh', '₹1.75 Lakh', '₹2 Lakh', 'Max']
        }
        
        # Determine the default min/max values based on the data
        default_min_index = 0
        default_max_index = len(price_options['Max']) - 1

        selected_min_price_str = st.selectbox("Min Price", options=price_options['Min'], index=default_min_index)
        selected_max_price_str = st.selectbox("Max Price", options=price_options['Max'], index=default_max_index)
        
        min_price_inr = lakh_to_inr(selected_min_price_str)
        max_price_inr = lakh_to_inr(selected_max_price_str) if selected_max_price_str != 'Max' else df['Price (Rs)'].max()


        # 2. Brand Multi-select
        st.subheader("🏢 Brand & Utility")
        all_brands = sorted(df['Brand'].unique())
        selected_brands = st.multiselect(
            "Brand",
            options=all_brands,
            default=all_brands
        )

        # 3. Utility Multi-select
        all_utilities = sorted(df['Utility'].unique())
        selected_utilities = st.multiselect(
            "Utility/Usage",
            options=all_utilities,
            default=all_utilities
        )

        # 4. RAM and Storage
        st.subheader("💾 Core Specs")
        # RAM Filter
        all_ram = sorted(df['RAM (GB)'].unique())
        min_ram_val = st.select_slider(
            "Minimum RAM (GB)",
            options=all_ram,
            value=all_ram[0]
        )

        # Storage Filter
        all_storage = sorted(df['Storage (GB)'].unique())
        min_storage_val = st.select_slider(
            "Minimum Storage (GB)",
            options=all_storage,
            value=all_storage[0]
        )
        
        # 5. CPU Filters
        st.subheader("🧠 CPU Specs")
        all_cpu_brands = sorted(df['CPU Brand'].unique())
        selected_cpu_brands = st.multiselect(
            "CPU Brand",
            options=all_cpu_brands,
            default=all_cpu_brands
        )

        # 6. GPU Filters
        st.subheader("🎮 Graphics Specs")
        gpu_type_options = ['Dedicated', 'Integrated']
        selected_gpu_type = st.multiselect(
            "Graphics Type",
            options=gpu_type_options,
            default=gpu_type_options
        )
        
        all_vram = sorted(df[df['GPU VRAM (GB)'] > 0]['GPU VRAM (GB)'].unique())
        min_vram_val = st.select_slider(
            "Minimum Dedicated VRAM (GB)",
            options=[0] + list(all_vram),
            value=0
        )
        
        # 7. Screen Filter
        st.subheader("🖥️ Screen Size")
        screen_options = {
            "14 inch - 15 inch": (14.0, 15.0),
            "15 inch - 16 inch": (15.0, 16.0),
            "16 inch & Above": (16.0, 100.0), # Use 100 as a high max for "Above"
            "All Sizes": (0.0, 100.0)
        }
        
        selected_screen_range = st.selectbox(
            "Screen Size Range",
            options=list(screen_options.keys()),
            index=3
        )
        screen_min, screen_max = screen_options[selected_screen_range]

        # 8. Performance/Spec Score Filter
        st.subheader("⭐ Performance")
        min_score = int(df['Spec Score'].min())
        max_score = int(df['Spec Score'].max())
        score_value = st.slider(
            "Minimum Spec Score",
            min_value=min_score,
            max_value=max_score,
            value=min_score,
            step=1
        )


    # --- Apply Filters ---
    
    # Base Filtering
    filtered_df = df[
        (df['Price (Rs)'] >= min_price_inr) & 
        (df['Price (Rs)'] <= max_price_inr) &
        (df['Spec Score'] >= score_value) &
        (df['Brand'].isin(selected_brands)) &
        (df['Utility'].isin(selected_utilities)) &
        (df['RAM (GB)'] >= min_ram_val) &
        (df['Storage (GB)'] >= min_storage_val) &
        (df['CPU Brand'].isin(selected_cpu_brands)) &
        (df['Screen (in)'] >= screen_min) &
        (df['Screen (in)'] < screen_max + 0.001) # Use a tiny offset for inclusive max
    ]
    
    # GPU Type Filtering (Handle Integrated vs. Dedicated Logic)
    if 'Dedicated' in selected_gpu_type and 'Integrated' not in selected_gpu_type:
        filtered_df = filtered_df[filtered_df['GPU Dedicated'] == 'Dedicated']
    elif 'Integrated' in selected_gpu_type and 'Dedicated' not in selected_gpu_type:
        filtered_df = filtered_df[filtered_df['GPU Dedicated'] == 'Integrated']
    # If both or neither selected, no filter is applied by default

    # Minimum VRAM filtering (only applies to dedicated GPUs)
    if 'Dedicated' in selected_gpu_type and min_vram_val > 0:
         filtered_df = filtered_df[filtered_df['GPU VRAM (GB)'] >= min_vram_val]


    # --- Display Results ---
    st.subheader(f"✅ Showing **{len(filtered_df)}** Laptops Matching Your Criteria")
    
    if filtered_df.empty:
        st.warning("No laptops match the current selection. Try broadening your filters!")
    else:
        # --- Visualization Section (Price vs. Performance) ---
        st.markdown("### 📈 Price vs. Performance Scatter Plot")
        
        # Calculate Price/Score ratio for coloring (lower is better value)
        # Add 1 to price to avoid division by zero (though prices are high enough)
        filtered_df['Value Score (Lower is better)'] = filtered_df['Price (Rs)'] / filtered_df['Spec Score']

        fig = px.scatter(
            filtered_df.reset_index(),
            x="Price (Rs)",
            y="Spec Score",
            color="Value Score (Lower is better)",
            size="RAM (GB)",
            color_continuous_scale=px.colors.sequential.Viridis_r, # Reverse Viridis so lower value is better (darker)
            hover_name="Name",
            hover_data={
                "Price (Rs)": ':,.0f', 
                "Spec Score": True, 
                "RAM (GB)": True,
                "Storage (GB)": True,
                "GPU VRAM (GB)": True,
                "CPU Full Model": True,
                "Value Score (Lower is better)": ':.0f'
            },
            template="plotly_white",
            title="Price vs. Spec Score: Visualizing Value"
        )
        fig.update_layout(
            height=600, 
            xaxis_title="Price (INR)", 
            yaxis_title="Spec Score (Performance)",
            coloraxis_colorbar_title="Value Score"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Data Table Section ---
        st.markdown("### 📋 Detailed Filtered Data")
        
        # Select and format columns for display
        display_cols = [
            "Brand", "Utility", "Price (Rs)", "Spec Score", 
            "CPU Full Model", "RAM (GB)", "Storage (GB)", 
            "GPU Type", "GPU VRAM (GB)", "Screen (in)"
        ]
        
        st.dataframe(
            filtered_df[display_cols].sort_values(by=['Spec Score', 'Price (Rs)'], ascending=[False, True]), 
            use_container_width=True,
            column_config={
                "Price (Rs)": st.column_config.NumberColumn("Price (Rs)", format="₹%d"),
                "Screen (in)": st.column_config.NumberColumn("Screen (in)", format="%.1f in"),
            }
        )

        # --- Download Button ---
        csv = convert_df_to_csv(filtered_df.reset_index())
        st.download_button(
            label="⬇️ Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_laptops_advanced.csv',
            mime='text/csv',
            key='download-csv-advanced'
        )

if __name__ == "__main__":
    main()