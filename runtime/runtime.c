#include<stdio>


//messages

typedef enum{
	AUDIO_PCM,
	TRANSCRIPTION,
	AI_TOKEN,
	TTS_SENTENCE,
	INTERRUPT,
	METRIC,
}MESSAGE_TYPE;


//logger

bool DEBUG=false;

void debug(char** message){
	if DEBUG
		printf("\n[DEBUG] %s\n",message);
}
void info(char** message){
	printf("[INFO] %s\n",message);
}

void error(char** message){
	printf("[ERROR] %s",message);
}



