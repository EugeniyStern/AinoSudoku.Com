import ezdxf
import svgwrite
import numpy as np

#  https://www.desmos.com/calculator/rtkn6udxmy

# r=-\ 0.0\cdot\cos\left(2\cdot\theta\right)\ -\ \ 0.02\cdot\cos\left(4\cdot\theta\ \right)\ \ +\ 0.0\ \cos\ \left(6\cdot\theta\right)\ +\ 0.1\cos\left(8\cdot\left(\theta\right)\right)\ +\frac{5}{\left|\cos\left(\theta+\frac{\pi}{4}\right)\right|\ +\ \left|\sin\left(\theta+\frac{\pi}{4}\right)\right|}

# r=-\ 0.0\cdot\cos\left(2\cdot\theta\right)\ -\ \ 0.02\cdot\cos\left(4\cdot\theta\ \right)\ \ +\ 0.0\ \cos\ \left(6\cdot\theta\right)\ +\ 0.1\cos\left(8\cdot\left(\theta\right)\right)\ +\frac{5}{\left|\cos\left(\theta+\frac{\pi}{4}\right)\right|\ +\ \left|\sin\left(\theta+\frac{\pi}{4}\right)\right|}

# r\ =5-\cos\left(\theta\cdot2\right)\cdot0.5-0.3\cdot\cos\left(\theta\cdot4\right)+0.1\cdot\cos\left(6\theta\right)


def init_files():
    svg_file = svgwrite.Drawing('svgwrite-example.svg', profile='tiny', viewBox=('0 0 1500 1500'))
    dxf_file = ezdxf.new('R2000')
    return svg_file, dxf_file


def polar_func_square(alfa):
    s2s2 = np.sqrt(2.0)
    R = s2s2 / (abs(np.cos(alfa + np.pi / 4)) + abs(np.sin(alfa + np.pi / 4)))
    return np.cos(alfa) * R, np.sin(alfa) * R


def polar_func_device_shape(alfa):
    s2s2 = np.sqrt(2.0)
    R = s2s2 / (abs(np.cos(alfa + np.pi / 4)) + abs(np.sin(alfa + np.pi / 4))) + 0.01 * np.cos(14 * alfa)
    return np.cos(alfa) * R, np.sin(alfa) * R


def polar_func_device_3hole(alfa):
    R = 5 / (abs(np.cos(alfa + np.pi / 4)) + abs(np.sin(alfa + np.pi / 4))) - 0.025 * np.cos(4 * alfa) + 0.25 * np.cos(12 * alfa) + 0.1 * np.cos(10 * alfa)
    R = R / 3.68
    return np.cos(alfa) * R, np.sin(alfa) * R


def polar_func_lamp(alfa):
    R = 5 - 0.5 * np.cos(2 * alfa) - 0.3 * np.cos(4 * alfa) + 0.1 * np.cos(6 * alfa)
    R = R / 5
    return np.cos(alfa) * R, np.sin(alfa) * R


def polar_func_lamp_b(alfa):
    R = 5 / (abs(np.cos(alfa + np.pi / 4)) + abs(np.sin(alfa + np.pi / 4))) - 0.04 * np.cos(6 * alfa) + 0.05 * np.cos(8 * alfa) 
    R = R * 0.276
    return np.cos(alfa) * R, np.sin(alfa) * R


def draw_fig_half_with_internal(N_of_points, x0, y0, R, kx, ky, polar_func, R_i, kx_i, ky_i, polar_func_int, alfa_shift_a):

    points = []
    points_np = np.zeros((N_of_points * 4 + 6), dtype=np.float32)
    L = 0
    x = 0
    y = 0
    
    for i in range(N_of_points + 1):
        alfa = alfa_shift_a + i / N_of_points * np.pi

        x_prev = x
        y_prev = y
        
        x, y = polar_func(alfa)
         
        x = int(kx * R * x * 100) / 100 + x0
        y = int(ky * R * y * 100) / 100 + y0
      
        if i > 0:
            L += np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))
        else:
            x_first = x
            y_first = y

        points_np[i * 2] = x
        points_np[i * 2 + 1] = y
        points.append((x, y))
        
#         internal part
    for i in range(N_of_points + 1):
        alfa = alfa_shift_a + (N_of_points - i) / N_of_points * np.pi

        x_prev = x
        y_prev = y
        
        x, y = polar_func_int(alfa)
         
        x = int(kx_i * R_i * x * 100) / 100 + x0
        y = int(ky_i * R_i * y * 100) / 100 + y0
      
        if i > 0:
            L += np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))

        points_np[N_of_points * 2 + 2 + i * 2] = x
        points_np[N_of_points * 2 + 3 + i * 2 ] = y
        
        points.append((x, y))
        
    points_np[N_of_points * 4 + 4 ] = x_first
    points_np[N_of_points * 4 + 5 ] = y_first
    points.append((x_first, y_first))
        
    return points, points_np, L


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
         
        x = int(kx * R * x * 100) / 100 + x0
        y = int(ky * R * y * 100) / 100 + y0
      
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

        
def add_path(svg_file, dxf_msp, points, points_np):
    dxf_msp.add_lwpolyline(points)
    svg_path = build_svg_path(points_np)
    svg_file.add(svg_file.path(d=svg_path,
            stroke="#000",
            fill="none",
            stroke_width=0.1))  


def panel(svg_file, msp, L, Center_X, Center_Y, outline):
    
   
# Device shape
    points, points_np, dl = draw_figure(N_of_points=256, x0=Center_X, y0=Center_Y, R=0.5, kx=380, ky=372, polar_func=polar_func_device_shape)
    L += dl
    add_path(svg_file, msp, points, points_np)
    
# # Board outline
    if outline == 1:
        points, points_np, dl = draw_figure(N_of_points=256, x0=Center_X, y0=Center_Y, R=0.5, kx=342, ky=327.4, polar_func=polar_func_square)
        L += dl
        add_path(svg_file, msp, points, points_np)
    
    B3_X_step = 36 * 3
    B3_Y_step = 36.4 * 3
    
    X_step = 36
    Y_step = 36.4
    
    for i in range(3):
        for j in range(3):
            ij = i * 10 + j
            if ij == 0 or ij == 11 or ij == 22:
                for ii in range(3):
                    for jj in range(3):
                        CX = (i - 1) * B3_X_step + (ii - 1) * X_step + Center_X
                        CY = (j - 1) * B3_Y_step + (jj - 1) * Y_step + Center_Y
#                         Small hole for lamp
                        kx = 32
                        points, points_np, dl = draw_figure(N_of_points=128, x0=CX, y0=CY, R=0.5, kx=kx, ky=32, polar_func=polar_func_lamp)
                        L += dl
                        add_path(svg_file, msp, points, points_np)                        
            if ij == 21 or ij == 12 or ij == 1 or ij == 10:
                CX = (i - 1) * B3_X_step + Center_X
                CY = (j - 1) * B3_Y_step + Center_Y
                
                points, points_np, dl = draw_figure(N_of_points=128, x0=CX, y0=CY, R=0.5, kx=B3_X_step - 8, ky=B3_Y_step - 4, polar_func=polar_func_square)
                L += dl
                add_path(svg_file, msp, points, points_np)   
                
            if ij == 2 or ij == 20:
                for ii in range(3):
                    for jj in range(3):
                        CX = (i - 1) * B3_X_step + (ii - 1) * X_step + Center_X
                        CY = (j - 1) * B3_Y_step + (jj - 1) * Y_step + Center_Y
#                         Small hole for lamp
                        kx = 32
                        points, points_np, dl = draw_figure(N_of_points=128, x0=CX, y0=CY, R=0.5, kx=kx, ky=32, polar_func=polar_func_square)
                        L += dl
                        add_path(svg_file, msp, points, points_np)                
    return L


def main():
    svg_file, dxf_file = init_files()
    
    msp = dxf_file.modelspace()
    L = 0
    
# List outline
#     points, points_np, dl = draw_figure(N_of_points=256, x0=750, y0=750, R=0.5, kx=1500, ky=1500, polar_func=polar_func_square)
#     L += dl
#     add_path(svg_file, msp, points, points_np)    
    
    L = panel(svg_file, msp, L, Center_X = 220, Center_Y = 220, outline = 0 )
    L = panel(svg_file, msp, L, Center_X = 220, Center_Y = 650, outline = 1 )
    
    for i in range(24):
        Center_X = 610 + i * 30
        Center_Y = 200 + i * 30
    
        points, points_np, dl = draw_fig_half_with_internal(N_of_points=256, x0=Center_X,
                                                            y0=Center_Y, R=0.5, kx=380,
                                                            ky=-372, polar_func=polar_func_device_shape,
                                                            R_i=0.5, kx_i=342, ky_i=-327.4,
                                                            polar_func_int=polar_func_square,
                                                            alfa_shift_a=np.pi / 4)
        add_path(svg_file, msp, points, points_np)
        L += dl
    
    
    for i in range(6):
        Center_X = 1300 - i * 30
        Center_Y = 200 + i * 30
    
        points, points_np, dl = draw_fig_half_with_internal(N_of_points=256, x0=Center_X,
                                                            y0=Center_Y, R=0.5, kx=-380,
                                                            ky=-372, polar_func=polar_func_device_shape,
                                                            R_i=0.5, kx_i=-342, ky_i=-327.4,
                                                            polar_func_int=polar_func_square,
                                                            alfa_shift_a=np.pi / 4)
        add_path(svg_file, msp, points, points_np)
        L += dl    
        
        
    for i in range(6):
        Center_X = 610 + i * 30
        Center_Y = 900 - i * 30
    
        points, points_np, dl = draw_fig_half_with_internal(N_of_points=256, x0=Center_X,
                                                            y0=Center_Y, R=0.5, kx=380,
                                                            ky=372, polar_func=polar_func_device_shape,
                                                            R_i=0.5, kx_i=342, ky_i=327.4,
                                                            polar_func_int=polar_func_square,
                                                            alfa_shift_a=np.pi / 4)
        add_path(svg_file, msp, points, points_np)
        L += dl          



#     My local laser cut service costs me ~1 USD per meter of length (plywood 10mm)
#           fanera3d.ru
    Center_X = 220
    Center_Y = 1050
    points, points_np, dl = draw_figure(N_of_points=256, x0=Center_X, y0=Center_Y, R=0.5, kx=380, ky=372, polar_func=polar_func_device_shape)
    L += dl
    add_path(svg_file, msp, points, points_np)


    print(L)
    M = int((L * 64) / 1000)
    print('Rub =', M)
    
    dxf_file.saveas("lwpolyline1.dxf")
    
    svg_file.save()

        
if __name__ == '__main__':
    main()
        
