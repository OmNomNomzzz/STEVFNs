# Get involved


## Bug reports and functionality requests
If you wish to report bugs, have feedback, ways to improve, have requests for new functionality/assets, etc. please email the author Aniq Ahsan at aniq_ahsan@hotmail.com


## Ways you can contribute

There are three main users:
1. **System designers:** end-users of STEVFNs tool
2. **Asset Modellers:** researchers that wish to model new assets in the STEVFNs framework and implement it in the STEVFNs tool
3. **Optimizers:** researchers that wish to change or implement the solver used in the STEVFNs tool

If you are a _system designer_ and wish to use the tool for a case study. You may contact the author, Aniq Ahsan, at aniq_ahsan@hotmail.com They can provide free training for how to use the tool. Please cite the tool and relevant publications if you use the STEVFNs tool for your work.


If you are an _asset modeller_, please contact the author, Aniq Ahsan, at aniq_ahsan@hotmail.com They will give a free tutorial on how to define new assets in the STEVFNs framework so that they can be implemented in the tool. Please cite the tool and relevant publications if you implement new assets in the framework. If you wish to make your newly defined assets open source and added to the tool, please discuss it with Aniq.
These are some assets that are yet to be implemented:

1. Low temperature heating
2. Ammonia production that needs to be run at constant rate
3. Building that requires cooling and/or heating
4. Conventional power generator with ramp-rate constraints
5. DCOPF or DC approximation of electricity lines


If you are an _optimizer_, please contact the author, Aniq Ahsan, at aniq_ahsan@hotmail.com They will discuss new solvers that can be implemented in the STEVFNs tool.

These are some ideas that are yet to be implemented:

1. SCS gpu solver. (I am having some issues trying to get it to run with cvxpy).
2. Custom convex optimization on parallel architecture like a GPU.

## Other contributions

**UI/UX improvements:**
The current UI/UX is very bare bones. If you wish to add a nice UI for building a system, adding assets, etc. please contact Aniq.

**Data management:**
Currently, when the case study is changed, the scenarios need to be changed manually. I wish to integrate snakemake to the workflow. If you wish to contribute to this, please contact Aniq.
