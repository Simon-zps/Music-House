import React from "react";
import { Link, useParams } from 'react-router-dom';
import { useState, useEffect } from "react";
import { Grid, Button, Typography } from '@material-ui/core';
import CreateRoom from "./CreateRoom";
import Player from "./Player";

export default function Room(props) {

    let {code} = useParams();
    const [message, setMessage] = useState("");
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestPausePermission, setGuestPausePermission] = useState(true);
    const [isHost, setIsHost] = useState(true);
    const [isAuthenticated, setAuthenticated] = useState(false);
    const [showSettings, setShowSettings] = useState(false); // relates to showing the actual settings page, not button
    const [song, setSong] = useState("");
    
    //We need to fetch data regarding that code and display info, useEffect with empty array runs once

    // TODO Use of async/await: When working with promises, it's better to use async/await instead of .then() for better readability and error handling.

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
            if(data.is_host){
                authenticateSpotifyUser();
            }
        });

        getCurrentSong();
        const intervalId = setInterval(() => {
            getCurrentSong();
            console.log("refreshing");
        }, 2000); // fetch song data every 5 seconds
        return () => clearInterval(intervalId);
        // clean up the interval when component is unmounted
        
    }, [message]);

    function getCurrentSong() {
        fetch("/spotify/current-song")
            .then(response => {
                if (!response.ok) {
                    return;
                }
                return response.json();
                
            })
            .then((data) => {
                setSong(data);
                console.log("Song:", data.title);
            });
    }

    function handleChangeCode(newValue) {
        props.onChange(newValue);
        window.history.pushState({}, "","/");
    }

    function leaveRoom() {
        fetch(`/api/leave-room/${code}`,{
            method:"POST",
            headers: {
                'Content-Type':'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            handleChangeCode(data.code);
            window.location.href = "/";
        });
    }

    function authenticateSpotifyUser(){
        fetch('/spotify/is-auth')
        .then(response => response.json())
        .then(data=>{
            setAuthenticated(data.status);
            if(!data.status){
                fetch('/spotify/get-auth')
                .then(response=>response.json())
                .then((data)=>{
                    window.location.replace(data.url);
                });
            }
        });
    }

    if(showSettings) {
        return (
            <Grid container spacing={0}>
                <Grid item xs={12} align="center">
                    <CreateRoom setMessage={setMessage} message={message} update={true} votesToSkip={votesToSkip} guestPausePermission={guestPausePermission} code={code}></CreateRoom>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={()=>setShowSettings(false)}>Close</Button>
                </Grid>
            </Grid>
        );
    }
    
    
    return (
        <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">Room code: {code}</Typography>
            </Grid>

            <Player {...song}/>
            
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">Song: {song.title}</Typography>
            </Grid>

            { isHost && (
                <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={()=>{setShowSettings(true)}}>Settings</Button>
                </Grid>
            ) }

            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveRoom} >Leave room</Button>
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