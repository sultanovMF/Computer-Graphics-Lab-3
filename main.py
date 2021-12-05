# Вариант 4
import sys
import numpy as np
import pygame
from pygame.locals import *
from numpy.linalg import norm
# Константы
width = 800
height = 800
m = 7


def translate(radius_vector, Tx, Ty):
    transformation_matrix = np.array([[1, 0, Tx],
                                      [0, 1, Ty],
                                      [0, 0, 1]])
    return np.matmul(transformation_matrix, radius_vector)


def rotate(radius_vector, angle):
    transformation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                      [np.sin(angle), np.cos(angle), 0],
                                      [0, 0, 1]])
    return np.matmul(transformation_matrix, radius_vector)

def scale(radius_vector, scale_coefficient):
    transformation_matrix = np.array([[scale_coefficient, 0, 0],
                                      [0, scale_coefficient, 0],
                                      [0, 0, 1]])
    return np.matmul(transformation_matrix, radius_vector)

def shear(radius_vector, relate_to_vector):
    angle_rotate = np.arctan(float(relate_to_vector[1][0]) / relate_to_vector[0][0]) + np.pi
    rotate_matrix_plus = np.array([[np.cos(angle_rotate), -np.sin(angle_rotate), 0],
                                      [np.sin(angle_rotate), np.cos(angle_rotate), 0],
                                      [0, 0, 1]])
    angle_rotate *= -1             
    
    rotate_matrix_minus = np.array([[np.cos(angle_rotate), -np.sin(angle_rotate), 0],
                                      [np.sin(angle_rotate), np.cos(angle_rotate), 0],
                                      [0, 0, 1]])
    
    tg_angle_sheer = float(radius_vector[1][0]) / radius_vector[0][0]

    shear_matrix = np.array([[1, tg_angle_sheer, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]])                      
    transformation_matrix = np.matmul(rotate_matrix_minus, shear_matrix)
    transformation_matrix = np.matmul(transformation_matrix, rotate_matrix_plus)

    return np.matmul(transformation_matrix, radius_vector)


def shear_polygon(list_of_polygon_coordinates, relate_to_vactor):
    result  = []
    for point in list_of_polygon_coordinates:
        result.append(shear(point, relate_to_vactor))
    return result


def translate_polygon(list_of_polygon_coordinates, Tx, Ty):
    result  = []
    for point in list_of_polygon_coordinates:
        result.append(translate(point, Tx, Ty))
    return result

def rotate_polygon_relate_to_point(list_of_polygon_coordinates, point, angle):
    Tx = point[0][0]
    Ty = point[1][0]
    result_translated = []
    for point in list_of_polygon_coordinates:
        result_translated.append(translate(point, -Tx, -Ty))
    
    result_rotated = []

    for point in result_translated:
        result_rotated.append(rotate(point, angle))
    
    result_translated = []
    for point in result_rotated:
        result_translated.append(translate(point, Tx, Ty))

    return result_translated

def scale_polygon_relate_to_point(list_of_polygon_coordinates, point, scale_coefficient):
    Tx = point[0][0]
    Ty = point[1][0]
    result_translated = []
    for point in list_of_polygon_coordinates:
        result_translated.append(translate(point, -Tx, -Ty))
    
    result_scaled = []

    for point in result_translated:
        result_scaled.append(scale(point, scale_coefficient))
    
    result_translated = []
    for point in result_scaled:
        result_translated.append(translate(point, Tx, Ty))

    return result_translated

def find_center_of_mass(list_of_polygon_coordinates):
    center_of_mass = np.array([[0], [0], [1]], dtype='float64')
    for coordinate in list_of_polygon_coordinates:
        center_of_mass += coordinate
    return (center_of_mass / m).astype(int)

def change_coordinate_system(radius_vector):
    transformation_matrix = np.array([[1, 0, width // 2],
                                      [0, -1, height // 2],
                                      [0, 0, 1]])
    return np.matmul(transformation_matrix, radius_vector)

def to_plain(radius_vector):
    return (radius_vector[0][0], radius_vector[1][0])


def transform_coordinates(radius_vector):
    return to_plain(change_coordinate_system(radius_vector))


def draw_polygon(surface, color, list_of_polygon_coordinates):
    for i in range(0, m - 1):
        start_point = transform_coordinates(list_of_polygon_coordinates[i])
        end_point = transform_coordinates(list_of_polygon_coordinates[i + 1])
        pygame.draw.line(surface, color, start_point, end_point)

    start_point = transform_coordinates(list_of_polygon_coordinates[-1])
    end_point = transform_coordinates(list_of_polygon_coordinates[0])
    pygame.draw.line(surface, color, start_point, end_point)

if __name__ == "__main__":
    pygame.init()
    # Константы
    width = 800
    height = 800
    surface = pygame.display.set_mode((width, height))
    m = 7
    dx = 5
    scale_step = 0.05
    angle_step = np.pi / 72

    relate_to_vector = np.array([[1], [-1], [1]])
    Tx = 0
    angle = 0
    scale_coefficient = 1
    sign = -1


    list_of_polygon_coordinates = [np.array([[-100], [200], [1]]),
                                   np.array([[50], [300], [1]]),
                                   np.array([[150], [200], [1]]),
                                   np.array([[300], [300], [1]]),
                                   np.array([[300], [-300], [1]]),
                                   np.array([[0], [-300], [1]]),
                                   np.array([[-300], [0], [1]])]

    
    center_of_mass = find_center_of_mass(list_of_polygon_coordinates)
    list_of_polygon_coordinates = scale_polygon_relate_to_point(list_of_polygon_coordinates, center_of_mass, 0.1)
   
    scale_coefficient = 1.0
    scale_step = 0.05
    sign = -1
    mode = 0
    #list_of_polygon_coordinates = scale_relate_co_center_of_mass(list_of_polygon_coordinates, scale_coefficient)
    result_polygon = list_of_polygon_coordinates

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                Tx = 0
                angle = 0
                scale_coefficient = 1
                sign = -1
                # Масштабирование относительно центра масс
                if event.key == pygame.K_0:
                    result_polygon = list_of_polygon_coordinates
                    mode = 0
                if event.key == pygame.K_1:
                    mode = 1

                if event.key == pygame.K_2:
                    mode = 2
    
                if event.key == pygame.K_3:
                    mode = 3

                if event.key == pygame.K_4:
                    mode = 4
        surface.fill((0,0,0))

         # Рисование системы координат
        pygame.draw.line(surface, (255, 255, 255),
                        (width // 2, 0), (width // 2, height))
        pygame.draw.line(surface, (255, 255, 255),
                        (0, height // 2), (width, height // 2))
        
        # рисование прямой y = 0.5 x
        pygame.draw.line(surface, (120, 0, 0),
                        (0, 600), (width, width / 4))
        

        # Рисование центра масс
        pygame.draw.circle(surface, (0, 0, 255), transform_coordinates(center_of_mass), 5)

        if mode == 1:
            if (scale_coefficient < 0 or scale_coefficient > 1.0):
                sign *= -1

            scale_coefficient += sign * scale_step
            result_polygon = scale_polygon_relate_to_point(list_of_polygon_coordinates, center_of_mass, scale_coefficient)

        if mode == 2:
            Tx += sign * dx
            Ty = 0.5 * (Tx)
            
            result_polygon = translate_polygon(list_of_polygon_coordinates, Tx, Ty)
            if (Tx < -90 or Tx > 90):
                sign *= -1
        
        if mode == 3:
            angle += angle_step
            result_polygon = rotate_polygon_relate_to_point(list_of_polygon_coordinates, center_of_mass, angle)

        if mode == 4:
            angle += sign * angle_step
            if (angle < - np.pi / 4 or angle > 0):
                sign *= -1
            
            relate_to_vector = rotate(relate_to_vector, angle)
            print(angle, relate_to_vector.flatten())
            result_polygon = shear_polygon(list_of_polygon_coordinates, relate_to_vector)

        pygame.time.wait(100)
        draw_polygon(surface, (255, 255, 255), result_polygon)
      #  draw_polygon(surface, (0, 120, 0), list_of_polygon_coordinates)
        pygame.display.update()
