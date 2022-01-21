# Examples and guidelines for modeling and solving combinatorial optimization problems with [IBM ILOG CP Optimizer](https://ibm.biz/CPOptimizer)

* Some material about CP Optimizer
   * [Python API](https://pypi.org/project/docplex/) of CP Optimizer
   * CP Optimizer [forum](https://ibm.biz/ConstraintProgForums)
   * Overview of CP Optimizer in [CONSTRAINTS Journal](https://ibm.biz/Constraints2018)
   * [Tutorial](material/cpotutorial-icaps-2017.pdf) on CP Optimizer at ICAPS 2017
   * CP Optimizer [documentation](https://ibm.biz/COS_Documentation)
* How to ...
   * [Typeset models](./how_to/typeset_models/README.md)
   * Model ...
      * [The Basics](./how_to/model/the_basics/README.md): optional interval variables, precedence and logical constraints, basic expressions
      * Some classical patterns
         * Allocation with alternative constraints
         * Chains of optional interval variables
         * [Work-Breakdown Structures](./how_to/model/work_breakdown_structures/README.md)
      * Classical machine scheduling problems
         * [Job-shop](./how_to/model/classical_scheduling_problems/job_shop/README.md)
         * [Open-shop](./how_to/model/classical_scheduling_problems/open_shop/README.md)
         * [Flow-shop](./how_to/model/classical_scheduling_problems/flow_shop/README.md)
         * [Flow-shop with earliness/tardiness cost](./how_to/model/classical_scheduling_problems/flow_shop_earliness_tardiness/README.md)
         * [Permutation flow-shop](./how_to/model/classical_scheduling_problems/permutation_flow_shop/README.md)
         * [Hybrid flow-shop](./how_to/model/classical_scheduling_problems/hybrid_flow_shop/README.md)
         * [Flexible job-shop](./how_to/model/classical_scheduling_problems/flexible_job_shop/README.md)
         * [Flexible job-shop with sequence-dependent setup times](./how_to/model/classical_scheduling_problems/flexible_job_shop_setup_times/README.md)
      * Classical project scheduling problems
         * [Resource-Constrained Project Scheduling Problem (RCPSP)](./how_to/model/classical_scheduling_problems/RCPSP/README.md)
         * [Resource-Constrained Project Scheduling Problem with max delays (RCPSP/MAX)](./how_to/model/classical_scheduling_problems/RCPSP_max/README.md)
         * [Multi-Mode Resource-Constrained Project Scheduling Problem (MM-RCPSP)](./how_to/model/classical_scheduling_problems/RCPSP_multi_mode/README.md)
         * [Resource-Constrained Project Scheduling Problem with discounted cash flows (RCPSPDC)](./how_to/model/classical_scheduling_problems/RCPSPDC/README.md)
      * Satellite scheduling
         * [Oversubscribed satellite scheduling](./how_to/model/oversubscribed_satellite/README.md)
         * Satellite observations scheduling (GEOCAPE)
      * Semiconductor manufacturing
         * [Simplified photolitography machine](./how_to/model/simplified_photolithography_machine/README.md)
         * [Semiconductor manufacturing](./how_to/model/semiconductor_manufacturing/README.md)
      * Uncertainties and robustness
         * Two-stage stochastic job-shop scheduling problem
         * [Two-stage stochastic programming and recoverable robustness](./how_to/model/recoverable_robustness/README.md)
      * Assembly line balancing
         * [Simple assembly line balancing (SALBP)](./how_to/model/assembly_line_balancing/README.md)
      * Energy-aware scheduling
         * [Jobshop with energy pricing](./how_to/model/jobshop_energy_pricing/README.md)
      * Miscellaneous scheduling problems
         * [Parallel machine scheduling](./how_to/model/parallel_machines/README.md)
         * [Mixed Resource Allocation and Scheduling](./how_to/model/mixed_resource_allocation_scheduling/README.md)
         * [Battery-operated machines](./how_to/model/battery_operated_machine/README.md)
