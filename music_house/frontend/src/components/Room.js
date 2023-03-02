import React from "react";
import { Link, useParams } from 'react-router-dom';
import { useState, useEffect } from "react";
import { Grid, Button, Typography } from '@material-ui/core';
export default function Room() {

    let {code} = useParams();
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestPausePermission, setGuestPausePermission] = useState(true);
    const [isHost, setIsHost] = useState(true);
    //We need to fetch data regarding that code and display info, useEffect with empty array runs once

    useEffect(() => {
        fetch(`/api/room/${code}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            setGuestPausePermission(data.guest_pause_permission);
            setIsHost(data.is_host);
            setVotesToSkip(data.votes_to_skip);
            console.log(data);
        });
    }, []);

    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">Room code: {code}</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Guest can pause: {guestPausePermission.toString()}</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Votes to skip: {votesToSkip}</Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="h5" component="h5">Is Host: {isHost.toString()}</Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" to="/" component={Link}>Leave room</Button>
            </Grid>
        </Grid>
    );
}
/*<div id="room-info">
            <p>Room code: {code}</p>
            <p>Guest can pause: {guestPausePermission.toString()}</p>
            <p>Votes to skip: {votesToSkip}</p>
            <p>Is Host: {isHost.toString()}</p>
        </div>*/