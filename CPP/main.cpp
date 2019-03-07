#include <iostream>
#include <fstream>
#include <vector>
#include <mgl2/mgl.h>

void print(double* p, int n) {
    for(int i = 0; i < n; i++) {
        std::cout << p[i] << std::endl;
    }
}

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
    /*
    // DEBUGGING CODE HERE
    std::cout << "XP" << std::endl;
    print(xp, m*n);
    std::cout << "YP" << std::endl;
    print(yp, m*n);
    std::cout << "ZP" << std::endl;
    print(zp, m*n);
    std::cout << "Coords" << std::endl;
    print(coords, 2*m*n);
    */

    // plot data
    mglGraph gr;

    gr.SetSize(1000,1000);

    gr.StartGIF("output.gif");

    mglData uu(m*n, xp);
    mglData vv(m*n, yp);
    mglData ww(m*n, zp);

    mglData tr = mglTriangulation(uu,vv);

    std::cout << "Coordinates using for axis:" << std::endl;
    std::cout << minx << " " << maxx << "/" << miny << " " << maxy << "/" << minz << " " << maxz << std::endl;

    for(double i = 0; i<360.0; i+=360.0 / FRAME_COUNT) {
        gr.NewFrame();

        gr.SetRanges(minx, maxx, miny, maxy, minz, maxz);
        //rotate around:  X Z Y
        gr.Rotate(45, i, 0);
        gr.Aspect(1,1,1); // set axis equal aspect
        gr.Axis();
        gr.TriPlot(tr,uu,vv,ww,"b");
        gr.TriPlot(tr,uu,vv,ww,"k#");
        //gr.TriCont(tr,uu,vv,ww,"B"); // contour lines

        gr.EndFrame();

        std::cout << "Current angle: " << i << std::endl;
    }

    gr.CloseGIF();

    delete[] xp;
    delete[] yp;
    delete[] zp;
    delete[] coords;

    return 0;
}
