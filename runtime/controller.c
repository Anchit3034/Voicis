#include<stdio.h>
//Event enum

typedef enum{
	SPEECH_STARTED, // =0
	SPEECH_FINISHED, //automatic =(prev+1)
    	TRANSCRIPTION_READY,
    	RESPONSE_READY,
    	INTERRUPT,
}Event;

//Runtime_state

typedef enum{
	IDLE,
	LISTENING,
	PROCESSING,
	SPEAKING,
}runtime_state;

