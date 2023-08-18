import matplotlib.pyplot as plt

def plot_arrow(s, e, filename):
    # 創建一個新的圖形
    plt.figure()

    # 繪製箭頭圖
    plt.arrow(s[0], s[1], e[0] - s[0], e[1] - s[1], head_width=0.5, head_length=0.4, fc='blue', ec='blue')

    # 設置圖形的範圍和標籤
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.xlabel('i')
    plt.ylabel('j')

    # 將圖片存為文件
    plt.savefig(filename)

    # 關閉圖形
    plt.close()

# 定義起始點 i 和終點 j
i = 1
j = 3
s = (i, 0)
e = (0, j)

# 呼叫函式來繪製箭頭圖並存為圖片檔案
plot_arrow(s, e, 'arrow_plot.png')
