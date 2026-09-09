import streamlit as st
import pandas as pd
import numpy as np
import kagglehub
import os
path = kagglehub.dataset_download("rkiattisak/student-performance-in-mathematics")

print(os.listdir(path)
