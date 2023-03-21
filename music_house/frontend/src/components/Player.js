import React, { Component } from "react"; 
import { Grid, Typography, Card, IconButton, LinearProgress, Collapse } from "@material-ui/core"; 
import { PlayArrow, SkipNext, Pause} from "@material-ui/icons";
import { useState, useEffect } from "react";

export default function Player(props) {

    const songProgress = (props.progress / props.duration) * 100;

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
                        <IconButton>
                            {props.is_playing ? <Pause/> : <PlayArrow/> }
                        </IconButton>
    
                        <IconButton>
                            <SkipNext/>
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant="determinate" value={songProgress}/>
        </Card>
    );
    
}
