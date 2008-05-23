#if !defined(invertor_h)
#define invertor_h


typedef struct {
    double d_max;
    double *x;
    double *y;
    double *err;
    int npoints;    
    int ny;    
    int nerr;  
    double alpha;
    double q_min;
    double q_max;
} Invertor_params; 

void invertor_dealloc(Invertor_params *pars);

void invertor_init(Invertor_params *pars);


double pr_sphere(double R, double r);
double ortho(double d_max, int n, double r);
double ortho_transformed(double d_max, int n, double q);
double ortho_derived(double d_max, int n, double r);
double iq(double *c, double d_max, int n_c, double q);
double pr(double *c, double d_max, int n_c, double r);
double dprdr(double *pars, double d_max, int n_c, double r);
double reg_term(double *pars, double d_max, int n_c, int nslice);
double int_p2(double *pars, double d_max, int n_c, int nslice);
void pr_err(double *pars, double *err, double d_max, int n_c, 
		double r, double *pr_value, double *pr_value_err);
int npeaks(double *pars, double d_max, int n_c, int nslice);
double positive_integral(double *pars, double d_max, int n_c, int nslice);
double positive_errors(double *pars, double *err, double d_max, int n_c, int nslice);

#endif
