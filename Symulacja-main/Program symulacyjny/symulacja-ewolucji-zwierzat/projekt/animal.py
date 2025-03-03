import random
import pygame
import math


"""klasa główna zwierząt"""
class Animal:
    MAX_HUNGER = 400
    MAX_HYDRATION = 400

    """inicjalizacja zwierzęcia"""
    def __init__(self, x, y, speed, hunger, hydration, vision):
        self.x = x
        self.y = y
        self.speed = speed
        self.hunger = hunger
        self.hydration = hydration
        self.vision = vision
        self.reproduction_cooldown = 30

    """rysowanie zwierzęca"""
    def draw(self, surface, grid_size):
        color = (255,255,255)
        radius = grid_size // 2
        center = (self.x * grid_size + radius, self.y * grid_size + radius)
        pygame.draw.circle(surface, color, center, radius)
        eye_radius = radius // 5
        eye_offset_x = radius // 2
        eye_offset_y = -radius // 3
        left_eye_center = (center[0] - eye_offset_x, center[1] + eye_offset_y)
        right_eye_center = (center[0] + eye_offset_x, center[1] + eye_offset_y)
        pygame.draw.circle(surface, (255, 255, 255), left_eye_center, eye_radius)
        pygame.draw.circle(surface, (255, 255, 255), right_eye_center, eye_radius)
        vision_width = self.vision * 2 + 1
        vision_height = self.vision * 2 + 1
        top_left_x = (self.x - self.vision) * grid_size
        top_left_y = (self.y - self.vision) * grid_size
        """pygame.draw.circle(surface, (255, 0, 0), center, self.vision * grid_size, 2)"""

    """metoda zwracajaca wspolrzedne zwierzecia"""
    def get_position(self):
        return (self.x, self.y)
    
    """poruszanie się zwierzęcia w losowym kierunku"""
    def move_randomly(self, x_grid_size, y_grid_size, occupiedWater):

        valid_positions = []

        for _ in range(10):
            new_x = self.x + random.randint(-2, 2)
            new_y = self.y + random.randint(-2, 2)
            if (new_x, new_y) not in occupiedWater and 0 <= new_x < x_grid_size and 0 <= new_y < y_grid_size:
                valid_positions.append((new_x, new_y))

        if valid_positions:
            new_x, new_y = random.choice(valid_positions)
            self.x = new_x
            self.y = new_y
            self.lose_energy()

    """poruszanie się w kierunku pożywienia - metoda używana w seekEnergy"""
    def move_towards(self, target_x, target_y, terrains):
        if self.x < target_x:
            next_x = self.x + 1
            if not self.is_position_blocked(next_x, self.y, terrains):
                self.x = next_x

        elif self.x > target_x:
            next_x = self.x - 1
            if not self.is_position_blocked(next_x, self.y, terrains):
                self.x = next_x

        if self.y < target_y:
            next_y = self.y + 1
            if not self.is_position_blocked(self.x, next_y, terrains):
                self.y = next_y

        elif self.y > target_y:
            next_y = self.y - 1
            if not self.is_position_blocked(self.x, next_y, terrains):
                self.y = next_y

    """utrata energii zwierzęcia"""
    def lose_energy(self):
        self.hunger += -1
        self.hydration += -1

    """zyskiwanie nawodnienia"""
    def gain_hydration(self):
        self.hydration += 350
        self.hydration = max(0, min(self.hydration, self.MAX_HYDRATION))

    """zyskiwanie głodu"""
    def gain_hunger(self):
        self.hunger += 350
        self.hunger = max(0, min(self.hunger, self.MAX_HUNGER))

    """reprodukcja zwierząt"""
    def reproduce(self, animals_list):
        if self.hunger > 200 and self.hydration > 200 and self.reproduction_cooldown == 0:
            new_animal = type(self)(self.x, self.y, self.speed, random.randint(50, 100), random.randint(50, 100),
                                    self.vision)
            animals_list.append(new_animal)
            self.hunger -= 30
            self.hydration -= 30
            self.reproduction_cooldown = 10

    """odnawianie czasu do reprodukcji"""
    def cooldown(self):
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

    """sprawdzanie czy pozycja jest zablokowana"""
    def is_position_blocked(self, x, y, terrains):
        for terrain in terrains:
            if (x, y) in terrain.occupiedCoordinates:
                return True
        return False





"""klasa tworząca ofiarę"""
class Prey(Animal):
    """inicjalizacja ofiary"""
    def __init__(self, x, y, speed, hunger, hydration, vision, ):
        super().__init__(x, y, speed, hunger, hydration, vision)
    """nadpisuje metode draw - zmienia kolor na zielony, ealiacja polimorfizmu"""
    def draw(self, surface, grid_size):
        color = (0,255,0)
        radius = grid_size // 2
        center = (self.x * grid_size + radius, self.y * grid_size + radius)
        pygame.draw.circle(surface, color, center, radius)
        eye_radius = radius // 5
        eye_offset_x = radius // 2
        eye_offset_y = -radius // 3
        left_eye_center = (center[0] - eye_offset_x, center[1] + eye_offset_y)
        right_eye_center = (center[0] + eye_offset_x, center[1] + eye_offset_y)
        pygame.draw.circle(surface, (255, 255, 255), left_eye_center, eye_radius)
        pygame.draw.circle(surface, (255, 255, 255), right_eye_center, eye_radius)
        vision_width = self.vision * 2 + 1
        vision_height = self.vision * 2 + 1
        top_left_x = (self.x - self.vision) * grid_size
        top_left_y = (self.y - self.vision) * grid_size
    def flee_from_predator(self, predators_list, terrains, x_grid_size, y_grid_size):
        closest_predator = None
        min_distance = float('inf')

        for predator in predators_list:
            distance = math.sqrt((self.x - predator.x) ** 2 + (self.y - predator.y) ** 2)
            if distance < min_distance and distance <= self.vision:
                min_distance = distance
                closest_predator = predator

        if closest_predator:
            direction_x = self.x - closest_predator.x
            direction_y = self.y - closest_predator.y

            if direction_x != 0:
                direction_x = direction_x / abs(direction_x)
            if direction_y != 0:
                direction_y = direction_y / abs(direction_y)

            for _ in range(self.speed):
                new_x = self.x + int(direction_x)
                new_y = self.y + int(direction_y)

                if not self.is_position_blocked(new_x, new_y, terrains):
                    self.x = new_x
                    self.y = new_y
                else:
                    self.move_randomly(x_grid_size, y_grid_size, [predator.get_position() for predator in predators_list])

    def seek_energy(self, food_list, terrainsWater):
        closest_item = None
        min_distance = float('inf')
        closest_items = []

        if self.hunger < 40 or self.hydration < 40:
            if self.hunger < self.hydration:
                item_list = food_list
            else:
                item_list = terrainsWater
        else:
            return False

        for item in item_list:
            distance = math.sqrt((self.x - item.x) ** 2 + (self.y - item.y) ** 2)
            if distance < min_distance and distance <= self.vision:
                min_distance = distance
                closest_items = [item]
            elif distance == min_distance:
                closest_items.append(item)

        if closest_items:
            closest_item = random.choice(closest_items)
            if closest_item in food_list:
                self.move_towards(closest_item.x, closest_item.y, terrainsWater)
                if (self.x, self.y) == (closest_item.x, closest_item.y):
                    self.gain_hunger()
                    food_list.remove(closest_item)
                    return True
            elif closest_item in terrainsWater:
                self.move_towards(closest_item.x, closest_item.y, terrainsWater)
                distance = math.sqrt((self.x - closest_item.x) ** 2 + (self.y - closest_item.y) ** 2)
                if distance <= 1:
                    self.gain_hydration()
                    return True

        return False





"""klasa tworząca drapieżnika"""
class Predator(Animal):
    """inicjalizacja drapieżnika"""
    def __init__(self, x, y, speed, hunger, hydration, vision):
        super().__init__(x, y, speed, hunger, hydration, vision)
    """nadpisuje metode draw - zmienia kolor na czerwony, ealiacja polimorfizmu"""
    def draw(self, surface, grid_size):
            color = (255,0,0)
            radius = grid_size // 2
            center = (self.x * grid_size + radius, self.y * grid_size + radius)
            pygame.draw.circle(surface, color, center, radius)
            eye_radius = radius // 5
            eye_offset_x = radius // 2
            eye_offset_y = -radius // 3
            left_eye_center = (center[0] - eye_offset_x, center[1] + eye_offset_y)
            right_eye_center = (center[0] + eye_offset_x, center[1] + eye_offset_y)
            pygame.draw.circle(surface, (255, 255, 255), left_eye_center, eye_radius)
            pygame.draw.circle(surface, (255, 255, 255), right_eye_center, eye_radius)
            vision_width = self.vision * 2 + 1
            vision_height = self.vision * 2 + 1
            top_left_x = (self.x - self.vision) * grid_size
            top_left_y = (self.y - self.vision) * grid_size
    """inny cooldown dla drapieznikow"""
    def reproduce(self, animals_list):
        if self.hunger > 200 and self.hydration > 200 and self.reproduction_cooldown == 0:
            new_animal = type(self)(self.x, self.y, self.speed, random.randint(50, 100), random.randint(50, 100),
                                    self.vision)
            animals_list.append(new_animal)
            self.hunger -= 30
            self.hydration -= 30
            self.reproduction_cooldown = 60
    def seek_water(self, terrainsWater):
        closest_item = None
        min_distance = float('inf')
        closest_items = []

        if self.hydration < 40:
            item_list = terrainsWater
        else:
            return False

        for item in item_list:
            distance = math.sqrt((self.x - item.x) ** 2 + (self.y - item.y) ** 2)
            if distance < min_distance and distance <= self.vision:
                min_distance = distance
                closest_items = [item]
            elif distance == min_distance:
                closest_items.append(item)

        if closest_items:
            closest_item = random.choice(closest_items)
            self.move_towards(closest_item.x, closest_item.y, terrainsWater)
            distance = math.sqrt((self.x - closest_item.x) ** 2 + (self.y - closest_item.y) ** 2)
            if distance <= 1:
                self.gain_hydration()
                return True

        return False


    def follow(self, prey_x, prey_y, terrains):
        """
        podążanie za ofiarą
        """
        if self.x < prey_x:

            for i in range(self.speed):
                next_x = self.x + i + 1
                if not self.is_position_blocked(next_x, self.y, terrains):
                    self.x = next_x
                    break
        elif self.x > prey_x:

            for i in range(self.speed):
                next_x = self.x - i - 1
                if not self.is_position_blocked(next_x, self.y, terrains):
                    self.x = next_x
                    break

        if self.y < prey_y:
            for i in range(self.speed):
                next_y = self.y + i + 1
                if not self.is_position_blocked(self.x, next_y, terrains):
                    self.y = next_y
                    break
        elif self.y > prey_y:
            for i in range(self.speed):
                next_y = self.y - i - 1
                if not self.is_position_blocked(self.x, next_y, terrains):
                    self.y = next_y
                    break


