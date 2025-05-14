[GlobalParams]
  displacements = 'disp_x disp_y'
  large_kinematics = false

  stabilize_strain = true

  # xx xy xz yx yy yz zx zy zz
  constraint_types = 'strain none none none none none none none none'
  macro_gradient = hvar
  homogenization_constraint = homogenization
[]


[Variables]
  [./disp_x]
  [../]
  [./disp_y]
  [../]

  [./hvar]
    family = SCALAR
    order = FIRST
  [../]
[]


[Mesh]
  [generated]
    type = GeneratedMeshGenerator
    dim = 2
    nx = 256
    ny = 256
    xmax = 1
    ymax = 1
    elem_type = QUAD8
                show_info=true
                output=true
  []
  [subdomain_id]
    type = SubdomainPerElementGenerator
    input = generated
    subdomain_ids = {{subdomain_ids}}
  []
  # defining node sets for PBCs and preventing rigid body motion
        [origin_set]
                type=ExtraNodesetGenerator
                new_boundary = 'origin'
                coord = '0 0'
                input=subdomain_id
        []
        [xp_set]
                type=ExtraNodesetGenerator
                new_boundary = 'x_plus'
                coord = '1 0'
                input=origin_set
        []
        [yp_set]
                type=ExtraNodesetGenerator
                new_boundary = 'y_plus'
                coord = '0 1'
                input=xp_set
        []

[]


[Kernels]
  [./sdx]
    type = HomogenizedTotalLagrangianStressDivergence
    variable = disp_x
    component = 0
  [../]
  [./sdy]
    type = HomogenizedTotalLagrangianStressDivergence
    variable = disp_y
    component = 1
  [../]
[]


[ScalarKernels]
  [enforce]
    type = HomogenizationConstraintScalarKernel
    variable = hvar
  []
[]


[Materials]
  # orthotropic fill method
  [./elasticity_1]
    type = ComputeElasticityTensor
    C_ijkl = '{{C1111}} {{C1122}} {{C1133}} {{C2222}} {{C2233}} {{C3333}} {{C2323}} {{C3131}} {{C1212}}'
    fill_method=symmetric9
    block = 1
  [../]
  [./elasticity_0]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = {{E0}}
    poissons_ratio = {{P0}}
    block = 0
  [../]

  [./compute_stress]
    type = ComputeLagrangianLinearElasticStress
    output_properties = 'small_stress'
  [../]

  [./compute_strain]
    type = ComputeLagrangianStrain
    homogenization_gradient_names = 'homogenization_gradient'
    output_properties = 'total_strain'
  [../]

  [./compute_homogenization_gradient]
     type = ComputeHomogenizedLagrangianStrain
  [../]
[]


[BCs]
  [./Periodic]
    [./y]
      variable = disp_y
      auto_direction = 'x y'
    []
    [./x]
      variable = disp_x
      auto_direction = 'x y'
    []
  []

  # constrain rigid body motion by pinning the corners and origin
        [fix_origin_x]
                type = DirichletBC
                boundary = "origin"
                variable = disp_x
                value = 0
        []

        [fix_origin_y]
                type = DirichletBC
                boundary = "origin"
                variable = disp_y
                value = 0
        []

        [fix_x]
          type = DirichletBC
          boundary = "x_plus"
          variable = disp_x
          value = 0
        []

        [fix_y]
          type = DirichletBC
          boundary = "y_plus"
          variable = disp_y
          value = 0
        []
[]


[AuxVariables]
  [./stress_xx]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./stress_yy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./stress_xy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strain_xx]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strain_yy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strain_xy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  # for testing
  #[./strain_zz]
  #  order = CONSTANT
  #  family = MONOMIAL
  #[../]
  [./maxprincipal]
    order = CONSTANT
    family = MONOMIAL
  [../]
[]

[AuxKernels]
  [./stress_xx]
    type = RankTwoAux
    rank_two_tensor = pk1_stress
    variable = stress_xx
    index_i = 0
    index_j = 0
  [../]
  [./stress_yy]
    type = RankTwoAux
    rank_two_tensor = pk1_stress
    variable = stress_yy
    index_i = 1
    index_j = 1
  [../]
  [./stress_xy]
    type = RankTwoAux
    rank_two_tensor = pk1_stress
    variable = stress_xy
    index_i = 0
    index_j = 1
  [../]
  [./strain_xx]
    type=RankTwoAux
    rank_two_tensor = mechanical_strain
    variable = strain_xx
    index_i = 0
    index_j = 0
  [../]
  [./strain_yy]
    type=RankTwoAux
    rank_two_tensor = mechanical_strain
    variable = strain_yy
    index_i = 1
    index_j = 1
  [../]
  [./strain_xy]
    type=RankTwoAux
    rank_two_tensor = mechanical_strain
    variable = strain_xy
    index_i = 0
    index_j = 1
  [../]
  [./maxprincipal]
    type = RankTwoScalarAux
    rank_two_tensor = pk1_stress
    variable = maxprincipal
    scalar_type = MaxPrincipal
    block = 0
  [../]
[]

# 0.0002 vol avgd strain in x-dir
[UserObjects]
  [homogenization]
    type = HomogenizationConstraint
    targets = '0.0002'
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
[]


# post processing relevant values per element of the domain mesh
[VectorPostprocessors]
  [stress_xx]
    type = ElementValueSampler
    variable = 'stress_xx'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [stress_yy]
    type = ElementValueSampler
    variable = 'stress_yy'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [stress_xy]
    type = ElementValueSampler
    variable = 'stress_xy'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [strain_xx]
    type = ElementValueSampler
  C:\Users\jhur6\OneDrive\Documents\AFRL-GT_Project_Files\AFRL_Project\code\stress_yy_test.png  variable = 'strain_xx'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [strain_yy]
    type = ElementValueSampler
    variable = 'strain_yy'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [strain_xy]
    type = ElementValueSampler
    variable = 'strain_xy'
    sort_by = id
    outputs = csv
    execute_on = 'INITIAL LINEAR NONLINEAR'
  []
  [maxprincipal]
    type = ElementValueSampler
    variable = 'maxprincipal'
    sort_by = id
    outputs = csv
    execute_on = ' INITIAL LINEAR NONLINEAR'
  []
[]


[Executioner]
    type = Steady

    solve_type = 'pjfnk'
    line_search = 'bt'

    #petsc_options_iname = '-pc_type'
    #petsc_options_value = 'lu'

    petsc_options_iname = '-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold'
    petsc_options_value = 'hypre     boomeramg      0.5'

    reuse_preconditioner = true
    reuse_preconditioner_max_linear_its = 10

    l_max_its = 100
    l_tol = 1e-10
    nl_rel_tol = 1e-8
    nl_max_its = 10

    automatic_scaling = true
    # scale contributions from each disp var and imposed strain independently
    scaling_group_variables = 'disp_x ; disp_y; hvar'
[]


[Outputs]
  file_base = 'out_files/{{out_dir}}/{{base_name}}'
  exodus = true
  csv = true
[]


[Debug]
  show_material_props = true
[]
