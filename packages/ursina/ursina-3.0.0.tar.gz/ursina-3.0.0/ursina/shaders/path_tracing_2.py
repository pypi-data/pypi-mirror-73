fragment_code = fragment='''
#version 420
#define MOTIONBLUR
#define CUBEMAPSIZE 256

#define SAMPLES 8
#define PATHDEPTH 4
#define TARGETFPS 60.

#define RAYCASTSTEPS 20
#define RAYCASTSTEPSRECURSIVE 2

#define EPSILON 0.001
#define MAXDISTANCE 180.
#define GRIDSIZE 8.
#define GRIDSIZESMALL 5.9
#define MAXHEIGHT 30.
#define SPEED 1.0

float time;


in float iTime;
in float iFrame;
in vec2 iResolution;

in vec2 fragCoord;
out vec4 fragColor;

//
// math functions
//

float hash( const float n ) {
	return fract(sin(n)*43758.54554213);
}
vec2 hash2( const float n ) {
	return fract(sin(vec2(n,n+1.))*vec2(43758.5453123));
}
vec2 hash2( const vec2 n ) {
	return fract(sin(vec2( n.x*n.y, n.x+n.y))*vec2(25.1459123,312.3490423));
}
vec3 hash3( const vec2 n ) {
	return fract(sin(vec3(n.x, n.y, n+2.0))*vec3(36.5453123,43.1459123,11234.3490423));
}
//
// intersection functions
//

float intersectPlane( const vec3 ro, const vec3 rd, const float height) {
	if (rd.y==0.0) return 500.;
	float d = -(ro.y - height)/rd.y;
	if( d > 0. ) {
		return d;
	}
	return 500.;
}

float intersectUnitSphere ( const vec3 ro, const vec3 rd, const vec3 sph ) {
	vec3  ds = ro - sph;
	float bs = dot( rd, ds );
	float cs = dot( ds, ds ) - 1.0;
	float ts = bs*bs - cs;

	if( ts > 0.0 ) {
		ts = -bs - sqrt( ts );
		if( ts > 0. ) {
			return ts;
		}
	}
	return 500.;
}

//
// Scene
//

void getSphereOffset( const vec2 grid, out vec2 center ) {
	center = (hash2( grid+vec2(43.12,1.23) ) - vec2(0.5) )*(GRIDSIZESMALL);
}
void getMovingSpherePosition( const vec2 grid, const vec2 sphereOffset, out vec3 center ) {
	// falling?
	float s = 0.1+hash( grid.x*1.23114+5.342+74.324231*grid.y );
	float t = fract(14.*s + time/s*.3);

	float y =  s * MAXHEIGHT * abs( 4.*t*(1.-t) );
	vec2 offset = grid + sphereOffset;

	center = vec3( offset.x, y, offset.y ) + 0.5*vec3( GRIDSIZE, 2., GRIDSIZE );
}
void getSpherePosition( const vec2 grid, const vec2 sphereOffset, out vec3 center ) {
	vec2 offset = grid + sphereOffset;
	center = vec3( offset.x, 0., offset.y ) + 0.5*vec3( GRIDSIZE, 2., GRIDSIZE );
}
vec3 getSphereColor( const vec2 grid ) {
	vec3 col = hash3( grid+vec2(43.12*grid.y,12.23*grid.x) );
    return mix(col,col*col,.8);
}

vec3 getBackgroundColor( const vec3 ro, const vec3 rd ) {
	return 1.4*mix(vec3(.5),vec3(.7,.9,1), .5+.5*rd.y);
}

vec3 trace(const vec3 ro, const vec3 rd, out vec3 intersection, out vec3 normal,
           out float dist, out int material, const int steps) {
	dist = MAXDISTANCE;
	float distcheck;

	vec3 sphereCenter, col, normalcheck;

	material = 0;
	col = getBackgroundColor(ro, rd);

	if( (distcheck = intersectPlane( ro,  rd, 0.)) < MAXDISTANCE ) {
		dist = distcheck;
		material = 1;
		normal = vec3( 0., 1., 0. );
		col = vec3(.7);
	}

	// trace grid
	vec3 pos = floor(ro/GRIDSIZE)*GRIDSIZE;
	vec3 ri = 1.0/rd;
	vec3 rs = sign(rd) * GRIDSIZE;
	vec3 dis = (pos-ro + 0.5  * GRIDSIZE + rs*0.5) * ri;
	vec3 mm = vec3(0.0);
	vec2 offset;

	for( int i=0; i<steps; i++ )	{
		if( material == 2 ||  distance( ro.xz, pos.xz ) > dist+GRIDSIZE ) break; {
			getSphereOffset( pos.xz, offset );

			getMovingSpherePosition( pos.xz, -offset, sphereCenter );
			if( (distcheck = intersectUnitSphere( ro, rd, sphereCenter )) < dist ) {
				dist = distcheck;
				normal = normalize((ro+rd*dist)-sphereCenter);
				col = getSphereColor(pos.xz);
				material = 2;
			}

			getSpherePosition( pos.xz, offset, sphereCenter );
			if( (distcheck = intersectUnitSphere( ro, rd, sphereCenter )) < dist ) {
				dist = distcheck;
				normal = normalize((ro+rd*dist)-sphereCenter);
				col = getSphereColor(pos.xz+vec2(1.,2.));
				material = 2;
			}
			mm = step(dis.xyz, dis.zyx);
			dis += mm * rs * ri;
			pos += mm * rs;
		}
	}

	intersection = ro+rd*dist;

	return col;
}

vec2 rv2;

vec3 cosWeightedRandomHemisphereDirection2( const vec3 n ) {
	vec3  uu = normalize( cross( n, vec3(0.0,1.0,1.0) ) );
	vec3  vv = cross( uu, n );

	float ra = sqrt(rv2.y);
	float rx = ra*cos(6.2831*rv2.x);
	float ry = ra*sin(6.2831*rv2.x);
	float rz = sqrt( 1.0-rv2.y );
	vec3  rr = vec3( rx*uu + ry*vv + rz*n );

    return normalize( rr );
}


void main() {
	time = iTime;
    // vec2 q = fragCoord.xy/iResolution.xy;
    vec2 q = fragCoord.xy/iResolution.xy;
	vec2 p = -1.0+2.0*q;
	p.x *= iResolution.x/iResolution.y;

	vec3 col = vec3( 0. );

	// raytrace
	int material;
	vec3 normal, intersection;
	float dist;
	float seed = time+(p.x+iResolution.x*p.y)*1.51269341231;

	for( int j=0; j<SAMPLES + min(0,iFrame); j++ ) {
		float fj = float(j);


		rv2 = hash2( 24.4316544311*fj+time+seed );

		vec2 pt = p+rv2/(0.5*iResolution.xy);

		// camera
		vec3 ro = vec3( cos( 0.232*time) * 10., 6.+3.*cos(0.3*time), GRIDSIZE*(time/SPEED) );
		vec3 ta = ro + vec3( -sin( 0.232*time) * 10., -2.0+cos(0.23*time), 10.0 );

		float roll = -0.15*sin(0.5*time);

		// camera tx
		vec3 cw = normalize( ta-ro );
		vec3 cp = vec3( sin(roll), cos(roll),0.0 );
		vec3 cu = normalize( cross(cw,cp) );
		vec3 cv = normalize( cross(cu,cw) );

		vec3 rd = normalize( pt.x*cu + pt.y*cv + 1.5*cw );

		vec3 colsample = vec3( 1. );

		// first hit
		rv2 = hash2( (rv2.x*2.4543263+rv2.y)*(time+1.) );
		colsample *= trace(ro, rd, intersection, normal, dist, material, RAYCASTSTEPS);

		// bounces
		for( int i=0; i<(PATHDEPTH-1); i++ ) {
			if( material != 0 ) {
				rd = cosWeightedRandomHemisphereDirection2( normal );
				ro = intersection + EPSILON*rd;

				rv2 = hash2( (rv2.x*2.4543263+rv2.y)*(time+1.)+(float(i+1)*.23) );

				colsample *= trace(ro, rd, intersection, normal, dist, material, RAYCASTSTEPSRECURSIVE);
			}
		}
		colsample = sqrt(clamp(colsample, 0., 1.));
		if( material == 0 ) {
			col += colsample;
		}
	}
	col  /= float(SAMPLES);

	fragColor = vec4( col,1.0);
}
'''
from panda3d.core import Shader

camera_contrast_shader = Shader.make(Shader.SL_GLSL,
vertex='''
#version 420
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 fragCoord;


void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  fragCoord = p3d_MultiTexCoord0;
}
''',

fragment=fragment_code, geometry='')


if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    camera.shader = camera_contrast_shader

    t = 0
    frame = 0
    mat = camera.lens.getProjectionMat()

    camera.set_shader_input('iResolution', window.size)
    camera.set_shader_input('iTime', t)
    camera.set_shader_input('iFrame', frame)

    def update():
      global t, frame
      t += time.dt
      camera.set_shader_input('iTime', t)

      frame += 1
      camera.set_shader_input('iFrame', frame)


    EditorCamera()

    app.run()
