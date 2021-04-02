import ezdxf
import svgwrite
import numpy as np
from scipy.linalg._flapack import dlamch

# r=-\ 0.0\cdot\cos\left(2\cdot\theta\right)\ -\ \ 0.02\cdot\cos\left(4\cdot\theta\ \right)\ \ +\ 0.0\ \cos\ \left(6\cdot\theta\right)\ +\ 0.1\cos\left(8\cdot\left(\theta\right)\right)\ +\frac{5}{\left|\cos\left(\theta+\frac{\pi}{4}\right)\right|\ +\ \left|\sin\left(\theta+\frac{\pi}{4}\right)\right|}

# r=-\ 0.0\cdot\cos\left(2\cdot\theta\right)\ -\ \ 0.02\cdot\cos\left(4\cdot\theta\ \right)\ \ +\ 0.0\ \cos\ \left(6\cdot\theta\right)\ +\ 0.1\cos\left(8\cdot\left(\theta\right)\right)\ +\frac{5}{\left|\cos\left(\theta+\frac{\pi}{4}\right)\right|\ +\ \left|\sin\left(\theta+\frac{\pi}{4}\right)\right|}

# r\ =5-\cos\left(\theta\cdot2\right)\cdot0.5-0.3\cdot\cos\left(\theta\cdot4\right)+0.1\cdot\cos\left(6\theta\right)


def init_files():
    svg_file = svgwrite.Drawing('svgwrite-example.svg', profile='tiny', viewBox=('0 0 500 500'))
    dxf_file = ezdxf.new('R2000')
    return svg_file, dxf_file


def polar_func_ord(alfa):
    s2s2 = np.sqrt(2.0)
    
    R = s2s2 / (abs(np.cos(alfa + np.pi / 4)) + abs(np.sin(alfa + np.pi / 4))) + 0.01 * np.cos(14 * alfa)
    
    return np.cos(alfa) * R, np.sin(alfa) * R


def draw_figure(N_of_points, x0, y0, R, kx, ky, polar_func):

    points = []
    points_np = np.zeros((N_of_points * 2 + 2), dtype=np.float32)
    L = 0
    x = 0
    y = 0
    
    for i in range(N_of_points + 1):
        alfa = i / N_of_points * 2 * np.pi

        x_prev = x
        y_prev = y
        
        x, y = polar_func(alfa)
         
        x = kx * int(R * x * 100) / 100 + x0
        y = ky * int(R * y * 100) / 100 + y0
      
        if i > 0:
            L += np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))

        points_np[i * 2] = x
        points_np[i * 2 + 1] = y
        points.append((x, y))
        
    return points, points_np, L

    
def build_svg_path(points):
    counter = 0
    path = ''
    
    N = int(points.shape[0] / 2)
    
    for p in range(N):
        if counter == 0:
            path = path + 'M '
        else:
            path = path + 'L '
         
        path = path + str(points[p * 2]) + ' ' + str(points[p * 2 + 1])
        counter += 1
    
    return path
        

def main():
    svg_file, dxf_file = init_files()
    
    msp = dxf_file.modelspace()
    L = 0
    points, points_np, dl = draw_figure(N_of_points=256, x0=20, y0=20, R=148, kx=1.0, ky=1.0, polar_func=polar_func_ord)
    L += dl
    print(L)
    M = int((L * 64) / 1000)
    print('Rub =', M)
    msp.add_lwpolyline(points)
    
    dxf_file.saveas("lwpolyline1.dxf")
    
    svg_path = build_svg_path(points_np)
    
    svg_file.add(svg_file.path(d=svg_path,
            stroke="#000",
            fill="none",
            stroke_width=0.1))
    
    svg_file.save()

        
if __name__ == '__main__':
    main()
        
