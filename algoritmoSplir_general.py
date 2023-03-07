import cv2
import os
import numpy as np

#Algoritmo para la creación de los archivos V1,v2,v3 juntos a los split de cada sección
#Algoritmo sobre la imagen R-REG-NIR
#Algoritmo sobre la imagen G-REG-NIR
#Algoritmo sobre la imagen B-REG-NIR

def read_listfile(path):
    archivos=os.listdir(path) #Lee todos los archivos pero no hace confimarción 
    #print(archivos)           
    return archivos
#función limpia los demas archivos y solod eja los .tif y los jpg de la lista, esto para no involucrar
# a los archivos de loc que carga el dron, en el caso de ser un algoritmo general. 
def limpieza_nombres(lista):
    lis_jpg_tif=[]
    lis_jpg=[]
    for nombres in lista:
            #hacemos filtro de la lista
            #if not in funciona como: Si no esta en la lista
            #El split(".") divide la palabra en el punto y toma desde la parte de atras
            # por el -1
            if nombres.split(".")[-1].upper() in ["jpg","JPG","TIF","tif"]:
                lis_jpg_tif.append(nombres)
            if nombres.split(".")[-1].upper() in ["jpg","JPG"]:
                lis_jpg.append(nombres)
    return lis_jpg_tif,lis_jpg #Lista con los nombrs de todos los archivos jpg y tif
    
#Función obtiene lista con [nombre,i,j] a partir de la imagen del recorte 
def dato_recorte(nombre_imagen):
    return [nombre_imagen[0:8],nombre_imagen[9],nombre_imagen[11]]

def algoritmo_busqueda(nombre_imagen_jpg,list_particiones):
    #Primer for obtiene en x numero en la lista y en nomb_imgpar obtiene la lista de imagenes
    #En el segundo for se recorre esa lista para obtener en que carpeta esta
        for x,nomb_imgpar in enumerate(list_particiones):
            for recorrido in nomb_imgpar:
                
                if (nombre_imagen_jpg==recorrido):
                    return(int(x))

# Algoritmo de alineación de imágenes por medio del algoritmo SIFT p
# NOTA: Para que funcione con python 301. y opnecv 4.6.0 se pasa a la función f =cv2.2dfeatures.SIFT_create() a f =cv2.SIFT_create()
# Resultado despues del cambio: 
def estabilizador_imagen(imagen_base, imagen_a_estabilizar, radio = 0.75, error_reproyeccion = 4.0, coincidencias = False):
        """Esta clase devuelve una secuencia de imágenes tomadas de la cámara estabilizada con respecto a la primera imagen"""
        
        # Se obtienen los puntos deinterés
        
        (kpsBase, featuresBase) = obtener_puntos_interes(imagen_base)
        (kpsAdicional, featuresAdicional) = obtener_puntos_interes(imagen_a_estabilizar)
        # Se buscan las coincidencias        
        
        M = encontrar_coincidencias(imagen_base, imagen_a_estabilizar, kpsBase, kpsAdicional, featuresBase, featuresAdicional, radio)
        
        if M is None:
            print("pocas coincidencias")
            return None
        
        if len(M) > 4:
            # construct the two sets of points
            # M2 = cv2.getPerspectiveTransform(ptsA,ptsB)
            (H, status) = encontrar_H_RANSAC_Estable(M, kpsBase, kpsAdicional, error_reproyeccion)
            estabilizada = cv2.warpPerspective(imagen_base,H,(imagen_base.shape[1],imagen_base.shape[0]))
            return estabilizada
        print("sin coincidencias")
        return None
    #--------------------------------------------------------------------------
def obtener_puntos_interes(imagen):
    f =cv2.SIFT_create()
    (kps, features) =f.detectAndCompute(imagen, None)
    return kps, features

def encontrar_coincidencias(img1, img2, kpsA, kpsB, featuresA, featuresB, ratio):
        """Metodo para estimar la homografia"""
        
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
#        
#        # loop over the raw matches
        for m in rawMatches:
#            # ensure the distance is within a certain ratio of each
#            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        
#        print (matches)
        return matches
    
def encontrar_H_RANSAC_Estable( matches, kpsA, kpsB, reprojThresh):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""
        
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
            ptsB = np.float32([kpsB[i].pt for (i, _) in matches])
    
            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            
            return (H, status)
#algoritmo para split la iamgen
#Recibe (par_x,par_y,imagen_shape_)
def split_image(dez_x,dez_y,imagen,lista_split,dir_ori,dir_save,list_jpgandtif):
    # Se obtiene las dimensiones de la imagen
    tam_x,tam_y,tamz=imagen.shape
    # División de total de pixeles/ número de divisiones
    # Se obtiene el tamaño de cada sección
    div_x=round(tam_x/dez_x)
    div_y=round(tam_y/dez_y)
    # Realizamos una copia de la imagen ya qué si se hace un cambio en el parametro
    # El cambios e ve refljeado en la variable original. 

    # Espacio para alinear la imágen y copiar en la variable copia con la nueva franja de color
    # 9 es el número de imagenes jpg
    for i in range (9):
        img_RGB2 = cv2.imread(dir_ori+list_jpgandtif[(i*6)+0],1)
        img_RGB = cv2.imread(dir_ori+list_jpgandtif[(i*6)+0],0)
        img_GRE = cv2.imread(dir_ori+list_jpgandtif[(i*6)+2],0)
        img_BLU = cv2.imread(dir_ori+list_jpgandtif[(i*6)+1],0)
        img_NIR = cv2.imread(dir_ori+list_jpgandtif[(i*6)+5],0)
        img_RED = cv2.imread(dir_ori+list_jpgandtif[(i*6)+3],0)
        img_REG = cv2.imread(dir_ori+list_jpgandtif[(i*6)+4],0)
        name=list_jpgandtif[(i*6)+0].split(".")[0]
        """ cv2.imshow("imagenRGB",img_RGB2)
        cv2.waitKey(0) """
        height, width=img_RGB.shape
        #height=800
        #width=800
        #print(img_RGB.shape)
        b_RGB = cv2.resize(img_RGB, (width, height), interpolation=cv2.INTER_LINEAR)
        b_GRE = cv2.resize(img_GRE, (width, height), interpolation=cv2.INTER_LINEAR)
        base_NIR = cv2.resize(img_NIR, (width, height), interpolation=cv2.INTER_LINEAR)
        b_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        b_REG = cv2.resize(img_REG, (width, height), interpolation=cv2.INTER_LINEAR)
        b_BLU = cv2.resize(img_BLU, (width, height), interpolation=cv2.INTER_LINEAR)
        b_RGB2 = cv2.resize(img_RGB2, (width, height), interpolation=cv2.INTER_LINEAR)

        stb_GRE = estabilizador_imagen(b_GRE, base_NIR)
        stb_RGB = estabilizador_imagen(b_RGB, base_NIR)
        stb_RED = estabilizador_imagen(b_RED, base_NIR)
        stb_REG = estabilizador_imagen(b_REG, base_NIR)
        stb_BLU = estabilizador_imagen(b_BLU, base_NIR)
        stb_NIR=base_NIR
        stb_RGB2 = estabilizador_imagen(b_RGB2, base_NIR)

        """ print(stb_REG.dtype)
        print(stb_RGB.dtype) """
        nueva=cv2.merge([stb_BLU,stb_REG,stb_NIR])

        copia=nueva.copy()
        # Hacemos recorrido 
        #cv2.rectangle(copia,(100,100),(300,300),(255,0,0),2)

        for j in range(dez_y):
            for i in range (dez_x):
                if (div_x*(i+1)<=tam_x):
                    cuadro=copia[div_x*i:div_x*(i+1),j*div_y:div_y*(j+1)]
                    name_split=name.split(".")[0]+"_"+str(i)+"_"+str(j)+".jpg"
                    print(name_split)
                    indice=algoritmo_busqueda(name_split,lista_split)
                    print(indice)
                    print(archivos_split[indice])
                    print(f"{dir_save}{archivos_split[indice]}/{name_split}\n")
                    """ print(f"div_x*i {div_x*(i+1)} , div_y*j {div_y*(j+1)}") """
                    #cv2.rectangle(copia,(j*div_y,i*div_x),((1+j)*div_y,(i+1)*div_x),(255,0,0),2)
                    cv2.imwrite(dir_save+archivos_split[indice]+"/"+name_split,cuadro)

if __name__=="__main__":
    dir_main ="./PlanesVuelo/101FPLAN/"
    archivos=read_listfile(dir_main)
    #print(archivos)
    listp_filt_jpg_tif,listp_filt_jpg=limpieza_nombres(archivos)   #Obtenemos la matriz filtrada jpg_tif y jpg. 
    #print(listp_filt_jpg)

    dir_split ="./Imagenes_clasificadas_2/"
    archivos_split=read_listfile(dir_split)
    #print(archivos)
    #listp_split=limpieza_nombres(archivos_split)   #Obtenemos la matriz filtrada. 
    #print(archivos_split)
    #for 
    list_general=[]
    for carpeta_split in archivos_split:
        dir2=dir_split+carpeta_split
        leer=read_listfile(dir2)
        list_general.append(leer)
    """ print(archivos_split)
    print(type(list_general)) """
    """  print("+++++++++++++++++++++++")
    print(list_general[0][0]) """
    #la siguiente función da el indice de la carpeta donde se encuentra la imagen en archivos split
    """ indice=algoritmo_busqueda("DJI_0010_0_5.jpg",list_general)
    print(indice)
    print(archivos_split[indice]) """
    dir_sav="./Nuevas_imagenes/carp3/"
    print(listp_filt_jpg_tif)

    dir_act=dir_main+"/DJI_0010.JPG"
    leer_img=cv2.imread(dir_act)
    split_image(10,10,leer_img,list_general,dir_main,dir_sav,listp_filt_jpg_tif)