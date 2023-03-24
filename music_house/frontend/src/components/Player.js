import React, { Component } from "react"; 
import { Grid, Typography, Card, IconButton, LinearProgress, Collapse } from "@material-ui/core"; 
import { PlayArrow, SkipNext, Pause} from "@material-ui/icons";
import { useState, useEffect } from "react";

export default function Player(props) {

    const [isPlayingClicked, setPlayingClicked] = useState(false);
    const songProgress = (props.progress / props.duration) * 100;

    async function skipSong(){
        const response = await fetch('/spotify/skip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return await response.text();
    }

    async function pauseSong(){
        const response = await fetch('/spotify/pause', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return await response.text();
    }

    async function playSong(){
        const response = await fetch('/spotify/play', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return await response.text();;
    }

    return (
        <Card variant="outlined" style={{ width: '100%' }}>
            <Grid container alignItems="center">
                <Grid item align="center" xs={4}>
                    <img src={props.image_url} style={{ height: '100%', width: '100%', objectFit: 'cover' }}></img>
                </Grid>
    
                <Grid item align="center" xs={8}>
                    <Typography color="textSecondary">
                        {props.title}
                    </Typography>
    
                    <Typography color="textSecondary">
                        {props.artist}
                    </Typography>
    
                    <div>
                    <IconButton onClick={async () => {
                        if (isPlayingClicked) {
                            pauseSong();
                            setPlayingClicked(false);
                        } else {
                            playSong();
                            setPlayingClicked(true);
                        }
                    }}>
                        { !isPlayingClicked ? <Pause/> : <PlayArrow/> }
                    </IconButton>
                        {props.votes_submitted} / {props.votes_required}
                        <IconButton>
                            <SkipNext onClick={skipSong}/>
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress}/>
        </Card>
    );
    
}
