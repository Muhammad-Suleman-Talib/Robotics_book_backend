---
id: part1_chapter7
sidebar_position: 7
title: Degrees of Freedom and Coordinate Systems
---

# Degrees of Freedom and Coordinate Systems

This chapter delves into the topic of "Degrees of Freedom and Coordinate Systems" within the context of "Physical AI & Humanoid Robotics". Here, we explore the fundamental concepts, key principles, and practical applications related to this area.

## The Language of Robot Motion: Degrees of Freedom and Coordinate Systems

To precisely describe, control, and analyze the movement of humanoid robots, a clear understanding of Degrees of Freedom (DoF) and various coordinate systems is essential. DoF quantifies a robot's ability to move independently, while coordinate systems provide the spatial framework for defining positions and orientations. This chapter delves into these foundational concepts, illustrating their critical role in the design, kinematics, and control of humanoid robotics.

## Degrees of Freedom (DoF)

The Degrees of Freedom (DoF) of a robot (or any rigid body) refer to the minimum number of independent parameters required to uniquely define its position and orientation in space.

### DoF of a Rigid Body

*   **In 2D Space:** A rigid body in a plane has 3 DoF: 2 for translation (x, y) and 1 for rotation (about the z-axis).
*   **In 3D Space:** A rigid body in 3D space has 6 DoF: 3 for translation (x, y, z) and 3 for rotation (roll, pitch, yaw, or rotations about x, y, z axes). These rotations are often represented using Euler angles, quaternions, or rotation matrices.

### DoF of Robotic Joints

Each joint in a robot contributes to the overall DoF of the system. Common joint types include:

*   **Revolute Joint (Rotational Joint):** Allows relative rotation about a single axis. It has 1 DoF. (e.g., elbow, knee, shoulder pitch).
*   **Prismatic Joint (Translational Joint):** Allows relative linear motion along a single axis. It has 1 DoF. (Less common in humanoids, but sometimes used in mechanisms).
*   **Spherical Joint:** Allows rotation about three axes, often used to model hip or shoulder joints, providing 3 DoF. (e.g., ball-and-socket joint).

### Total DoF of a Humanoid Robot

The total DoF of a humanoid robot is the sum of the DoF of all its independent joints. Humanoids typically have a high number of DoF (e.g., 20-60+ DoF) to mimic human-like dexterity and movement, making their control and analysis complex. This high redundancy allows for greater flexibility and adaptability but also increases the complexity of motion planning and control.

## Coordinate Systems

Coordinate systems provide a reference framework to describe positions, orientations, and movements. In robotics, several coordinate systems are commonly used:

1.  **World Frame (Fixed Frame / Global Frame):**
    *   A stationary reference frame that is fixed in the environment. All other robot positions and orientations are typically described relative to this frame.
    *   Origin and orientation are chosen arbitrarily but consistently (e.g., origin at the center of the robot's base, z-axis up).

2.  **Base Frame (Robot Frame):**
    *   A coordinate frame attached to the robot's base. If the robot is mobile, this frame moves relative to the world frame. If the robot is fixed, the base frame often coincides with the world frame.

3.  **Joint Frames (Link Frames):**
    *   Each link in the robot's kinematic chain has an associated coordinate frame.
    *   These frames are defined relative to the previous link's frame and are used in forward and inverse kinematics calculations (e.g., using Denavit-Hartenberg parameters).

4.  **End-Effector Frame (Tool Frame):**
    *   A coordinate frame attached to the robot's end-effector (e.g., gripper, hand, foot, head).
    *   Its position and orientation are often the primary targets for robot tasks.

### Transformations Between Coordinate Systems

Robot control involves continuously transforming positions and orientations between these different coordinate systems. Homogeneous transformation matrices are the standard tool for this:

*   `T_A_B`: A matrix that transforms coordinates from frame B to frame A.
*   To find the pose of a point `P_C` in frame A, given its pose in frame C, and the transformation from C to B, and B to A:
    `P_A = T_A_B * T_B_C * P_C`

## Importance in Humanoid Robotics

*   **Kinematics:** Essential for both forward and inverse kinematics to map joint angles to end-effector poses and vice-versa.
*   **Motion Planning:** Defining target poses and planning collision-free paths in a consistent reference frame.
*   **Sensor Data Interpretation:** Converting sensor readings (e.g., camera data) from the sensor's local frame to the robot's base frame or world frame.
*   **Control:** Ensuring that desired movements are executed correctly by providing commands in the appropriate joint or Cartesian space.
*   **Balance and Stability:** Critical for defining the robot's center of mass and supporting polygon in a stable coordinate system, especially for bipedal locomotion.

## Demonstration: Robot Coordinate Systems

A visual demonstration of different coordinate frames and their transformations on a robot can greatly enhance understanding.

<div class="video-container">
  <iframe
    width="560"
    height="315"
    src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
  ></iframe>
</div>
_Replace `YOUR_VIDEO_ID` with the actual YouTube video ID._

## Diagram: Robot Coordinate Frames

A visual representation of different coordinate frames (world, base, joint, end-effector) on a robot, illustrating how they are defined and relate to each other.

![Robot Coordinate Frames](/img/robot_coordinate_frames.png)

## Code Example: 2D Coordinate Transformation

This pseudocode demonstrates a basic 2D coordinate transformation using a homogeneous transformation matrix, rotating and translating a point from one frame to another. This is a simplified version of the transformations used in forward kinematics.

```python
import numpy as np

def create_transformation_matrix_2d(rotation_angle_rad, translation_x, translation_y):
    """
    Creates a 2D homogeneous transformation matrix for rotation and translation.

    Args:
        rotation_angle_rad (float): Rotation angle in radians.
        translation_x (float): Translation in x-direction.
        translation_y (float): Translation in y-direction.

    Returns:
        np.array: A 3x3 homogeneous transformation matrix.
    """
    cos_theta = np.cos(rotation_angle_rad)
    sin_theta = np.sin(rotation_angle_rad)

    T = np.array([
        [cos_theta, -sin_theta, translation_x],
        [sin_theta,  cos_theta, translation_y],
        [0,          0,          1          ]
    ])
    return T

def transform_point_2d(transformation_matrix, point_coords):
    """
    Transforms a 2D point using a 2D homogeneous transformation matrix.

    Args:
        transformation_matrix (np.array): The 3x3 transformation matrix.
        point_coords (tuple or list): The (x, y) coordinates of the point.

    Returns:
        np.array: The transformed (x, y) coordinates.
    """
    # Convert point to homogeneous coordinates [x, y, 1]
    homogeneous_point = np.array([point_coords[0], point_coords[1], 1])
    
    # Apply transformation
    transformed_homogeneous_point = transformation_matrix @ homogeneous_point
    
    # Convert back to 2D coordinates
    return transformed_homogeneous_point[:2]

# --- Example Usage ---
if __name__ == "__main__":
    # Define a point in Frame B
    point_in_frame_B = (1.0, 0.5)
    print(f"Original point in Frame B: {point_in_frame_B}")

    # Define the transformation from Frame B to Frame A
    # Frame A is rotated by 30 degrees relative to B, and translated
    rotation_angle_radians = np.radians(30) # 30 degrees
    translation_x_A_B = 2.0
    translation_y_A_B = 1.0

    T_A_B = create_transformation_matrix_2d(rotation_angle_radians, translation_x_A_B, translation_y_A_B)
    print("\nTransformation Matrix from B to A:")
    print(T_A_B)

    # Transform the point from Frame B to Frame A
    point_in_frame_A = transform_point_2d(T_A_B, point_in_frame_B)
    print(f"\nTransformed point in Frame A: ({point_in_frame_A[0]:.2f}, {point_in_frame_A[1]:.2f})")

    # Another example: Rotate by -90 degrees and translate
    point_in_frame_C = (0.0, 3.0)
    rotation_angle_C_D = np.radians(-90)
    translation_x_C_D = -1.0
    translation_y_C_D = 0.0

    T_C_D = create_transformation_matrix_2d(rotation_angle_C_D, translation_x_C_D, translation_y_C_D)
    transformed_point_in_D = transform_point_2d(T_C_D, point_in_frame_C)
    print(f"\nOriginal point in Frame C: {point_in_frame_C}")
    print("Transformation Matrix from D to C:")
    print(T_C_D)
    print(f"Transformed point in Frame D: ({transformed_point_in_D[0]:.2f}, {transformed_point_in_D[1]:.2f})")
```
This example showcases the fundamental mathematical operation behind how robots track their position and manipulate objects in their environment by converting between different frames of reference.

## Key Concepts

*   **Degrees of Freedom (DoF):** Minimum independent parameters defining position and orientation.
*   **Revolute Joint:** 1 DoF rotational joint.
*   **Prismatic Joint:** 1 DoF translational joint.
*   **Spherical Joint:** 3 DoF rotational joint (e.g., hip, shoulder).
*   **World Frame:** Fixed global reference.
*   **Base Frame:** Robot's local reference.
*   **Joint/Link Frames:** Frames attached to robot segments.
*   **End-Effector Frame:** Frame at the robot's tool point.
*   **Homogeneous Transformation Matrices:** Used for transformations between frames.

## Advanced Topics

*   **Denavit-Hartenberg (DH) Parameters:** A standard convention for systematically assigning coordinate frames to robot links, simplifying kinematic analysis and transformation matrix derivation.
*   **Quaternions for Orientation:** An alternative to Euler angles or rotation matrices for representing 3D orientations, often preferred for their avoidance of gimbal lock and computational efficiency in interpolation.
*   **Kinematic Redundancy:** When a robot has more DoF than strictly necessary for a task, allowing for optimization of secondary objectives (e.g., obstacle avoidance, joint limits).
*   **Operational Space Control:** Controlling the robot's end-effector directly in Cartesian space, rather than individual joint angles, often relying on Jacobian matrices.

## Exercises

1.  A simplified humanoid arm has 3 revolute joints: a shoulder (pitch), an elbow (pitch), and a wrist (pitch). Assuming all joints rotate in the same plane, how many degrees of freedom does this arm have? If the arm is fixed to a stationary torso, what is the total DoF of the arm relative to the world?
2.  Research the "gimbal lock" problem in the context of Euler angles. Why are quaternions often preferred in robotics for orientation representation?

## Further Reading

*   [Robot Kinematics and Dynamics by Mark W. Spong](https://example.com/spong-kinematics)
*   [Introduction to Robotics by John J. Craig](https://example.com/craig-robotics)