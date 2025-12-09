---
id: part2_chapter7
sidebar_position: 7
title: Jacobians for Velocity and Force Analysis
---

# Jacobians for Velocity and Force Analysis

This chapter delves into the topic of "Jacobians for Velocity and Force Analysis" within the context of "Physical AI & Humanoid Robotics". Here, we explore the fundamental concepts, key principles, and practical applications related to this area.

## The Jacobian: Unlocking Robot Dynamics and Control

The Jacobian matrix is an indispensable mathematical tool in robotics, serving as a bridge between the joint space (angles and angular velocities) and the task space (end-effector position, orientation, and linear/angular velocities). For humanoid robots, which are characterized by numerous joints and complex movements, the Jacobian is critical for tasks such as velocity control, static force analysis, singularity detection, and manipulability analysis. This chapter will explore the concept of the Jacobian, its derivation, and its wide-ranging applications in understanding and controlling robot motion and interaction.

## What is the Jacobian Matrix?

The Jacobian matrix (`J`) is a matrix of partial derivatives that relates the differential changes in joint variables to the differential changes in the end-effector's pose (position and orientation) in Cartesian space. Essentially, it maps joint velocities to end-effector velocities:

`ẋ = J(q) ⋅ q̇`

Where:
*   `ẋ` is the vector of end-effector linear and angular velocities (e.g., `[vx, vy, vz, ωx, ωy, ωz]T`).
*   `J(q)` is the Jacobian matrix, which is a function of the current joint configuration `q`.
*   `q̇` is the vector of joint velocities (e.g., `[q̇1, q̇2, ..., q̇n]T`).

The size of the Jacobian matrix depends on the number of task space variables and the number of joints (degrees of freedom, DoF) of the robot. For a 6-DoF end-effector task in 3D space and an `n`-DoF robot, the Jacobian will be a 6 x `n` matrix.

## Applications of the Jacobian

1.  **Velocity Kinematics (Forward Velocity Kinematics):**
    *   Directly calculates the end-effector's linear and angular velocities given the joint velocities. Crucial for smooth trajectory tracking and control.

2.  **Inverse Velocity Kinematics:**
    *   Used to find the required joint velocities (`q̇`) to achieve a desired end-effector velocity (`ẋ`).
    *   `q̇ = J⁻¹(q) ⋅ ẋ` (if `J` is invertible).
    *   For redundant robots, the pseudo-inverse (`J⁺`) is often used, allowing for optimization of secondary tasks (e.g., `q̇ = J⁺ẋ + (I - J⁺J)ż`, where `(I - J⁺J)ż` is null-space motion).

3.  **Static Force Analysis:**
    *   The transpose of the Jacobian matrix (`Jᵀ`) relates forces/torques in joint space (`τ`) to forces/torques exerted by the end-effector in task space (`F`): 
        `F = J⁻ᵀ(q) ⋅ τ` or `τ = Jᵀ(q) ⋅ F` (for static equilibrium).
    *   This is crucial for understanding how much force a robot can exert and for implementing force control strategies.

4.  **Singularity Analysis:**
    *   As discussed in a previous chapter, kinematic singularities occur when the Jacobian matrix loses rank (i.e., its determinant is zero or near zero for square Jacobians).
    *   The Jacobian helps identify these configurations, which are problematic for control.

5.  **Manipulability Analysis:**
    *   The manipulability ellipsoid, derived from `J ⋅ Jᵀ`, graphically represents the robot's ability to move and orient its end-effector in different directions for a given joint configuration. It quantifies how "easily" the robot can move in various directions.

## Derivation of the Jacobian

The Jacobian can be derived using several methods, most commonly:

*   **Vector Cross Products (for Angular Velocity) and Partial Derivatives (for Linear Velocity):** For each joint, its contribution to the end-effector velocity is calculated.
*   **Homogeneous Transformation Matrices:** Using the derivatives of the transformation matrices.

For revolute joints, the column `j` of the Jacobian related to linear velocity is `z_j-1 x (pe - pj-1)` and for angular velocity is `z_j-1`. For prismatic joints, it's `z_j-1` for linear velocity and `0` for angular velocity.

## Importance in Humanoid Robotics

*   **Whole-Body Control:** Humanoids rely heavily on Jacobians for coordinating the many DoF to achieve complex tasks like walking, balancing, and manipulation while interacting with the environment.
*   **Force Control and Human-Robot Interaction:** Jacobians are fundamental for implementing compliant control strategies and ensuring safe physical interaction with humans by precisely controlling interaction forces.
*   **Dynamic Motion Generation:** For generating dynamic gaits or agile movements, the Jacobian helps in translating desired end-effector dynamics into joint torque commands.

## Jacobians in Robotics (Video)

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
_Replace `YOUR_VIDEO_ID` with a relevant YouTube video ID explaining Jacobian matrices in robotics._

## Code Snippet: 2R Planar Arm Jacobian Calculation (Pseudocode)

```python
# --- Conceptual Pseudocode: Jacobian for a 2R Planar Arm ---

import numpy as np

def calculate_jacobian_2r_arm(l1, l2, theta1, theta2):
    """
    Calculates the Jacobian matrix for a 2R planar robot arm.
    
    The end-effector position (x, y) is given by:
    x = l1 * cos(theta1) + l2 * cos(theta1 + theta2)
    y = l1 * sin(theta1) + l2 * sin(theta1 + theta2)

    The Jacobian J relates [dx, dy]T to [d_theta1, d_theta2]T:
    J = [[dx/d_theta1, dx/d_theta2],
         [dy/d_theta1, dy/d_theta2]]
    """
    J11 = -l1 * np.sin(theta1) - l2 * np.sin(theta1 + theta2)
    J12 = -l2 * np.sin(theta1 + theta2)
    J21 =  l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    J22 =  l2 * np.cos(theta1 + theta2)
    
    return np.array([[J11, J12], [J21, J22]])

def calculate_end_effector_velocity(jacobian_matrix, joint_velocities):
    """
    Calculates the end-effector velocity given the Jacobian and joint velocities.
    ẋ = J ⋅ q̇
    """
    return jacobian_matrix @ joint_velocities

# --- Main execution ---
if __name__ == "__main__":
    link1_length = 1.0  # meters
    link2_length = 0.8  # meters

    # Current joint configuration
    theta1_rad = np.radians(30) # 30 degrees
    theta2_rad = np.radians(45) # 45 degrees
    
    # Joint velocities
    q_dot = np.array([np.radians(10), np.radians(5)]) # 10 deg/s for J1, 5 deg/s for J2

    print("--- 2R Arm Jacobian and Velocity Analysis ---")
    
    # Calculate the Jacobian for the current configuration
    J = calculate_jacobian_2r_arm(link1_length, link2_length, theta1_rad, theta2_rad)
    print("\nJacobian Matrix for current configuration:")
    print(J)

    # Calculate the end-effector velocity
    x_dot = calculate_end_effector_velocity(J, q_dot)
    print(f"\nJoint velocities (rad/s): q̇1={q_dot[0]:.2f}, q̇2={q_dot[1]:.2f}")
    print(f"End-effector velocity (m/s): ẋx={x_dot[0]:.2f}, ẋy={x_dot[1]:.2f}")

    # Example: Check for singularity
    J_singular = calculate_jacobian_2r_arm(1.0, 1.0, 0, 0) # Fully extended arm
    print("\nJacobian for a singular configuration (fully extended):")
    print(J_singular)
    print(f"Determinant: {np.linalg.det(J_singular):.4f}")
```
This pseudocode demonstrates the calculation of the Jacobian matrix for a simple 2R planar arm and its application to determine the end-effector's velocity from given joint velocities. It also briefly touches upon how the Jacobian's determinant can indicate a singular configuration.

## Key Concepts

-   **Jacobian Matrix:** Relates joint velocities to end-effector velocities.
-   **Forward Velocity Kinematics:** Calculating end-effector velocity from joint velocities.
-   **Inverse Velocity Kinematics:** Calculating joint velocities from desired end-effector velocity.
-   **Static Force Analysis:** Relating joint torques to end-effector forces.
-   **Singularity Analysis:** Detecting configurations where the robot loses DoF.
-   **Manipulability Ellipsoid:** Visualizing robot dexterity.

## Advanced Topics

*   **Geometric vs. Analytical Jacobian:** Understanding different methods for deriving the Jacobian matrix.
*   **Joint-Space vs. Task-Space Control:** How the Jacobian bridges these two control domains, enabling Cartesian control by mapping to joint commands.
*   **Redundant Robot Control:** Utilizing the null space of the Jacobian to perform secondary tasks (e.g., obstacle avoidance, joint limit avoidance) without affecting the primary end-effector task.
*   **Dynamic Jacobian:** Extensions of the Jacobian concept to analyze and control robot dynamics, including considerations for mass and inertia.

## Exercises

1.  Derive the full 6xN Jacobian matrix for a 3-DOF robot arm with two revolute joints and one prismatic joint.
2.  Explain how the Jacobian matrix is used in an impedance control scheme for a robot interacting with its environment.

## Further Reading

-   [Robot Dynamics and Control by Mark W. Spong](https://example.com/spong-dynamics-control-jacobian)
-   [Robotics: Modelling, Planning and Control by Siciliano, Sciavicco, Villani, Oriolo](https://example.com/siciliano-robotics-jacobian)