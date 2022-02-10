import numpy as np
from numpy import exp, abs, sin, cos, tan, arcsin, arccos, arctan, pi, conj
import matplotlib.pyplot as plt
import random
plt.style.use('dark_background')

def if_float(expression): # Checks whether the equation is of type: x = constant
    try:
        float(expression)
        return(True)
    except ValueError:
        return(False)

def eqn_type(expression): # Returns the variable and the expression of the equation
    equation = list((expression.replace(' ', '')).split('='))
    var = str(equation[0])
    newexpression = str(equation[1])
    return(var, newexpression)

def transform(transfunc, xrange = [0], yrange = [0], n = 0, auxfunc = '0', x_aux = [0]):

    # Default Values
    if(xrange == [0]): xrange = [-5, 5]
    if(yrange == [0]): yrange = [-5, 5]
    if(n == 0): n = 50
    
    transformation = eval("lambda z:"+ transfunc)

    xaxis = np.linspace(xrange[0], xrange[1], n)
    yaxis = np.linspace(yrange[0], yrange[1], n)
    Xver, Yver = np.meshgrid(xaxis, yaxis)              # Vertical Grid Lines
    Xhor, Yhor = np.transpose(Xver), np.transpose(Yver) # Horizontal Grid Lines
    
    # Applying Transformation
    wver = transformation(Xver + 1j*Yver)
    whor = transformation(Xhor + 1j*Yhor)

    fig, ax = plt.subplots(1, 2)
    
    ax[0].plot(Xver, Yver, color = "#52B1D2", alpha = 0.5, zorder = 0)
    ax[0].plot(Xhor, Yhor, color = "#F48BA9", alpha = 0.5, zorder = 0)
    ax[1].plot(wver.real, wver.imag, color = "#52B1D2", alpha = 0.5, zorder = 0)
    ax[1].plot(whor.real, whor.imag, color = "#F48BA9", alpha = 0.5, zorder = 0)
    
    if(auxfunc != '0'):
        var_zoom = 1
        colors = ['orange', '#9FD96A', 'gold', 'white']

        # Checks the x range for the functions depending upon the input from the user.
        if(x_aux == [1]): 
            xaux = xaxis   # xaxis = [-5, 5, 50]
            var_zoom = 0
        elif(x_aux == [0]): 
            xaux = np.linspace(-1, 1, 50)  # Default Values
        else: 
            xaux = np.linspace(float(x_aux[0]), float(x_aux[1]), int(x_aux[2]))

        zoom_x = xaux
        i = 0
        for functions in auxfunc:
            x_aux = xaux
            var = eqn_type(functions)[0]    # Checks whether the equation is of type x = g(y) or y = f(x)
            expression = eqn_type(functions)[1]   # Returns f(x) or g(y)
            
            if(var == 'y'):
                if(if_float(expression) == True): # Checks if the equation is of type: y = constant
                    y_aux = float(expression)*np.ones(len(x_aux))
                else: 
                    aux_function = eval("lambda x:"+ (expression))
                    y_aux = aux_function(x_aux)    # y values for the corresponding x values

            elif(var == 'x'):
                y_aux = x_aux   # x is variable, y is constant
                if(if_float(expression) == True): # Checks if the equation is of type: x = constant
                    x_aux = float(expression)*np.ones(len(y_aux))
                else: 
                    aux_function = eval("lambda y:"+ (expression))
                    x_aux = aux_function(y_aux)    # x values for the corresponding y values
            
            waux = transformation(x_aux + 1j*y_aux)   # Transforming the z plane into w plane
            # colors = np.random.rand(1,3)       

            ax[0].plot(x_aux, y_aux, color = colors[i], label = "{:}".format(functions), zorder=10)            # Plots (x, y) in the z plane
            ax[1].plot(waux.real, waux.imag, color = colors[i], label = "{:}".format(functions), zorder=10)    # Plots the transformed func in w plane
            i += 1

        if (var_zoom != 0): xrange = [2*zoom_x[0], 2*zoom_x[-1]]
    
    elif(auxfunc == '0'):
        random_x, random_y = random.choice(xaxis/2), random.choice(yaxis/2)
        random_w = transformation(random_x + 1j*random_y)
        ax[0].scatter(random_x, random_y, c = "#9FD96A", label = "Random z", zorder= 10)        
        ax[1].scatter(random_w.real, random_w.imag, c = "#9FD96A", label = "w(z)", zorder=10)
    
    ax[0].set(title = "Input Space or Z - Plane", xlabel = "Real Axis of Z-Plane", ylabel = "Imaginary Axis of Z-Plane", xlim = 1.01*np.array(xrange), ylim = 1.01*np.array(yrange))
    ax[0].legend(loc = "upper right")
    ax[1].legend(loc = "upper right")
    ax[1].set(title = "Output Space or W - Plane", xlabel = "Real Axis of W-Plane", ylabel = "Imaginary Axis of W-Plane", xlim = 2*np.array(xrange), ylim = 2*np.array(yrange))    
    fig.suptitle("$w = f(z) = {:}}}$".format(transfunc.replace("**", "^{")))
    plt.show()

if __name__ == '__main__':
    run = 'y'
    print("\n\tAn applet for Complex Mapping, made by: Samarth Jain - https://github.com/theSamJain/Complex-Transformations\n")
    
    while(run == 'y'):
        transfunc = input("\nEnter the Transformation function: f(z) = ")
        
        print("\nEnter various parameters according to your choice. Type '0' to use default values.\n")
        
        xrange = list(map(float, (((input("Enter x range (default is [-5, 5]) = ")).strip("[")).strip("]")).split(",")))
        yrange = list(map(float, (((input("Enter y range (default is [-5, 5]) = ")).strip("[")).strip("]")).split(",")))
        n = int(input("Enter number of points on any one of the axes (default is 50) = "))

        func_n = int(input("\nEnter the number of Auxilary Functions you want (Type '0' to skip): "))

        if (func_n > 0):
            print("\nEnter expressions like: y = f(x) or x = g(y), where f and g can be functions or constants\n")
            auxfunc = []
            for i in range(func_n):
                eqn = str(input("Enter an Auxilary Function : "))
                auxfunc.append(eqn)
            x_aux = list(map(float, (((input("\nEnter x range for Auxilary Functions (default is [-1, 1, 50]. To use same as x range as above, type '1') = ")).strip("[")).strip("]")).split(",")))
        else:   
            auxfunc = '0'
            x_aux = [1]

        transform(transfunc, xrange, yrange, n, auxfunc, x_aux)
        run = input("Do you want to continue? y/n: ")