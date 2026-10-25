#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <string.h>
#include<unistd.h>

typedef struct{
    char id_video[10];
    char titulo[81];
    char nome_arquivo[101];
    char status[20];
} Registro;

int mudar_status_processando(Registro *registro, sqlite3 *db){
    int rc;
    char *msg = 0;
    char sql[120] = "UPDATE videos SET status='PROCESSANDO' WHERE id = ";
    strcat(sql, registro->id_video);
    strcat(sql, ";");
    rc = sqlite3_exec(db, sql, NULL, NULL, &msg);
        if(rc != SQLITE_OK){
            fprintf(stderr, "Erro ao executar a mudança de status!\n-> %s\n", msg);
            return 1;
        }
    return 0;
}

int mudar_status_finalizado(Registro *registro, sqlite3 *db){
    int rc;
    char *msg = 0;
    char sql[120] = "UPDATE videos SET status='FINALIZADO' WHERE id = ";
    strcat(sql, registro->id_video);
    strcat(sql, ";");
    rc = sqlite3_exec(db, sql, NULL, NULL, &msg);
        if(rc != SQLITE_OK){
            fprintf(stderr, "Erro ao executar a mudança de status!\n-> %s\n", msg);
            return 1;
        }
    return 0;
}

void converter(Registro *registro){
    char nome_arquivo[101];
    char cmd[2048] = "";
    char caminho_arquivo[1024] = "";
    char pasta_arquivo[100] = "";
    
    // caminho do arquivo
    strcpy(nome_arquivo, registro->nome_arquivo);
    strcat(caminho_arquivo, "../app/uploads/");
    strcat(caminho_arquivo, nome_arquivo);
    strcpy(pasta_arquivo, caminho_arquivo); // copiando apenas a pasta, sem o ext.mp4
    strcat(caminho_arquivo, "/ext.mp4 ");
    
    // criação do comando
    strcat(cmd, "ffmpeg -i ");
    strcat(cmd, caminho_arquivo);
    strcat(cmd, "-c:v libx264 -preset veryfast -crf 21 -g 60 -keyint_min 60 -sc_threshold 0 -c:a aac -b:a 128k -ac 2 -f hls -hls_time 6 -hls_playlist_type vod -hide_banner -loglevel error ");
    strcat(cmd, pasta_arquivo);
    strcat(cmd, "/index.m3u8");
    printf("Comando: %s\n", cmd);
    system(cmd);
}

int ler(void *n, int num_colunas, char **valores_linha, char **nome_colunas){
    Registro registro;
    for(int i = 0; i< num_colunas; i++){
        switch (i)
        {
        case 0:
            strcpy(registro.id_video, valores_linha[i]);
            break;
        case 1:
            strcpy(registro.titulo, valores_linha[i]);
            break;
        case 2:
            strcpy(registro.nome_arquivo, valores_linha[i]);
            break;
        case 4:
            strcpy(registro.status, valores_linha[i]);
            break;
        default:
            break;
        }
        
    }
    mudar_status_processando(&registro, n);
    converter(&registro);
    mudar_status_finalizado(&registro, n);
    return 0;
}

int main(){
    sqlite3 *db;
    char *msg = 0;
    int rc = sqlite3_open("../instance/project.db", &db);
    if(rc != SQLITE_OK){
        fprintf(stderr, "Arquivo não encontrado!\n");
        return 1;
    }
    while(1){
        rc = sqlite3_exec(db, "SELECT * FROM videos WHERE status = 'EM_ESPERA';", ler, db, &msg);
        if(rc != SQLITE_OK){
            fprintf(stderr, "Erro ao executar a consulta!\n-> %s\n", msg);
            return 1;
        }
        sleep(10);
    }
    return 0;
}