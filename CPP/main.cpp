#include <iostream>
#include <fstream>
#include <vector>
#include <mgl2/mgl.h>
#include "delaunator.hpp"
#include <iomanip>


int main(int argc, char const *argv[])
{
    // filename is first argument
    auto filename = argv[1];
    int FRAME_COUNT = atoi(argv[2]);

    std::cout << "Reading " << filename << std::endl;
    std::ifstream stream(filename);
    int n,m;
    stream >> n >> m;
    std::cout << "Read dimensions: " << n << " and " << m << std::endl;

    double* xp = new double[n*m];
    double* yp = new double[n*m];
    double* zp = new double[n*m];
    double* coords = new double[n*m*2];

    // now follow n*m lines
    double x,y,z;
    double minx, miny, minz;
    double maxx, maxy, maxz;
    minx = miny = minz = 100000000;
    maxx = maxy = maxz = 0;
    for(int i = 0; i < n*m; i++) {
        stream >> x;
        stream >> y;
        stream >> z;

        coords[2*i] = x;
        coords[2*i + 1] = y;

        if(x > maxx) maxx=x;
        if(y > maxy) maxy=y;
        if(z > maxz) maxz=z;
        if(x < minx) minx=x;
        if(y < miny) miny=y;
        if(z < minz) minz=z;

        xp[i] = x;
        yp[i] = y;
        zp[i] = z;
    }
    std::cout << "Read " << n*m << " lines successfully." << std::endl;

    // do delauny here
    //delaunator::Delaunator d(xy_coords);
    delaunator::Delaunator d(std::vector<double>(coords, coords+n*m));

    int count_trias = d.triangles.size();

    double* trias = new double[count_trias];

    for(int i = 0; i < count_trias; i++) {
        trias[i] = d.triangles[i];
    }

    // plot data
    mglGraph gr;

    gr.SetSize(1000,1000);

    gr.StartGIF("output.gif");
    
    mglData tt(count_trias, 3, trias);
    mglData uu(count_trias, xp); // or m*n, xp
    mglData vv(count_trias, yp);
    mglData ww(count_trias, zp);

    std::cout << minx << " " << maxx << "/" << miny << " " << maxy << "/" << minz << " " << maxz << std::endl;

    for(double i = 0; i<360.0; i+=360.0 / FRAME_COUNT) {
        gr.NewFrame();
        /*gr.SetRanges(*std::min_element(xp, xp+n*m), *std::max_element(xp, xp+n*m),
            *std::min_element(yp, yp+n*m), *std::max_element(yp, yp+n*m),
            *std::min_element(zp, zp+n*m), *std::max_element(zp, zp+n*m));*/
        gr.SetRanges(minx, maxx, miny, maxy, minz, maxz);
        //rotate around:  X Z Y
        gr.Rotate(45, i, 0);
        gr.Aspect(1,1,1); // set axis equal aspect
        gr.Axis();
        gr.TriPlot(tt,uu,vv,ww,"b");
        gr.TriPlot(tt,uu,vv,ww,"k#");
        gr.EndFrame();
        std::cout << "i: " << i << std::endl;
    }

    gr.CloseGIF();

    delete[] xp;
    delete[] yp;
    delete[] zp;
    delete[] coords;
    delete[] trias;

    return 0;
}
