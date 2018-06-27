####### PACKAGES
import math
from numpy import *

def multilinear_regression(Y,XX,*args):
	sy=Y.shape
	sx=XX.shape
	# nimp is the number of 'important' fitting parameters
	if len(args)>0:
		nimp=args[0]
	else:
		nimp=min(sx)
	# Making sure Y is a column vector
	ny=max(Y.shape)
	if min(sy)>1 and len(sy)>1:
		ValueError('Y must be a column vector')
	else:
		Y=ravel(Y)
	# Making sure X is a column vector of rows
	if len(sx)==1:
		if sx!=ny:
			ValueError('X should be a matrix with as many rows as Y has elements')
	elif len(sx)==2:
		if sx[0]!=ny:
			XX=XX.T
			sx=XX.shape
			print('Warning : transposing X to match shape of Y')
		elif sx[0]!=ny:
			ValueError('X should be a matrix with as many rows as Y has elements')
	# We add a '1' column to X
	X=ones((ny,sx[1]+1))
	X[:,1:]=XX
	sx=X.shape
	nx=sx[1]
	#Okidoki now we can prepare for regression
	chosable=ones((nx,1),bool)
	# flag which rows can be chosen : obviously those without variance
	for i in range(nx):
		varx=var(X[:,i])
		if varx==0:
			chosable[i]=False
		else:
			chosable[i]=True
	nvx=sum(chosable)
	bli=array(range(nx))
	if nimp>nvx:
		print('Warning : changing predictor number to number of variables')

	left=bli[chosable[:,0]]
	left_ix=chosable[:,0]
	hist=ravel(zeros((1,nimp),int))
	res=ravel(zeros((1,nimp)))
	Rsq=nan*ravel(zeros((nx-1,1)))
	linco=ravel(zeros((nx-1,1)))
	# Last touch
	# We remove the mean of Y
	M=array([X[:,0]]).T
	cte=linalg.lstsq(M,Y,rcond=None)[0]
	YY=Y-ravel(M)*cte
	# baseline error
	err0=var(Y)

	# We find best to worst predictor in X
	for ni in range(nimp):
		nvx=sum(left_ix)
		scores=ones((1,nvx))
		# computing errors for all rows of X
		for j in range(nvx):
			vec=array([0,left[j]])
			M=X[:,vec]
			coefs,dy=linalg.lstsq(M,YY,rcond=None)[:2]
			scores[0,j]=sum(dy)
		# finding smallest errors
		rk=argmin(scores)
		ix=left[rk]
		hist[ni]=ix
		vec=ravel(zeros((ni+2,1),int))
		vec[1:]=hist[0:(ni+1)]
		M=X[:,vec]
		coefs,dy=linalg.lstsq(M,Y,rcond=None)[:2]
		YY=Y-sum(M*coefs,1)
		res[ni]=sum(dy)
		# updating the variables that can still be used
		left_ix[ix]=False
		left=bli[left_ix]

	# We reorder the coefficient to the order of X columns
	hist=hist-1
	linco[hist]=coefs[1:]
	offset=coefs[0]
	res=1.0-res/err0
	# we compute how much each column of X contributes to decreasing the variance
	if nimp>1:
		res[1:]=res[1:]-res[0:(nimp-1)]
	Rsq[hist]=res
	return linco,offset,Rsq,hist
