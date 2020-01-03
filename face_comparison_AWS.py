import boto3

#################
# Funcao que retorna lista de objetos de um Bucket AWS S3
# sera' usado para listar todas as imagens na pasta Fraude mais a diante

def list_bucket_objects(bucket_name):

    # Acessa conteudo do bucket
    s_3 = boto3.client('s3')
    try:
        response = s_3.list_objects_v2(Bucket=bucket_name)
    except:
        pass
        return None

    # Caso tenho conteudo na pasta, retorna lista de itens
    if response['KeyCount'] > 0:
        nova_lista=list()
        
        for b in response['Contents']:
            nova_lista.append (b['Key'])
        
        return nova_lista

    return None



#################
# Funcao que compara uma foto no S3 com outras fotos de outra pasta
#
# Comparacao da foto tirada com arquivo de Fraude


def compare_faces(sourceFile):

    client=boto3.client('rekognition')
      
    # gera uma lista de fotos no bucket Fraudes
    lista=(list_bucket_objects('fraudes'))

    print (lista)

    # looping de comparacão caso lista > 0 ou seja: ja' existe pelo menos 1 foto de fraudador para comparar
    if len(lista)>0:
        contador = 0
        fotos = list()

        for fraudador in lista:
            print (fraudador)

            try:
                # try esta neste codigo pois caso nao exista foto na comparacao, gera erro   
                response=client.compare_faces(SimilarityThreshold=80,
                                            SourceImage={'S3Object':{'Bucket':'chkout','Name':sourceFile}},
                                            TargetImage={'S3Object':{'Bucket':'fraudes','Name':fraudador}})
            
                
                for faceMatch in response['FaceMatches']:
                    position = faceMatch['Face']['BoundingBox']
                    similarity = str(faceMatch['Similarity'])
                    print('The face at ' +
                        str(position['Left']) + ' ' +
                        str(position['Top']) +
                        ' matches with ' + similarity + '% confidence')

                    contador=contador + 1
                    fotos.append (str(fraudador))

            except:
                pass
                # segue o laco

        #return len(response['FaceMatches'])

        # Devolve total de fontos de fraude encontradas e lista dos nomes das fotos
        return (contador,fotos)          

def main():
    
    # Arquivo de comparacao
    sourceFile='L1-COMPRA.jpg'
    
    # Chama funcao
    face_matches,fotos=compare_faces(sourceFile)

    # imprime resultados da comparacao
    print("Face matches: " + str(face_matches))
    print("Seen:" + str(fotos))

    
if __name__ == "__main__":
    main()




