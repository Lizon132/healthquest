import React, { Component } from 'react';

class DistanceLogger extends Component {
  state = {
    isLogging: false,
    lastPosition: null,
    totalDistance: 0, // Total distance traveled in meters
    events: [],
  };

  startLogging = () => {
    this.setState({ isLogging: true, totalDistance: 0, lastPosition: null }, () => {
      this.watchId = navigator.geolocation.watchPosition(
        this.handlePositionChange,
        (error) => console.warn('Error watching position:', error),
        { enableHighAccuracy: true, distanceFilter: 10 } // Update every 10 meters
      );
    });
  };

  stopLogging = () => {
    navigator.geolocation.clearWatch(this.watchId);
    this.setState({ isLogging: false }, () => {
      // Log the total distance traveled as an event
      const distanceEvent = {
        time: new Date().toISOString(),
        eventType: 'distanceTraveled',
        completed: true,
        metrics: { distance: this.state.totalDistance }, // Distance in meters
      };
      console.log(distanceEvent); // Or process this event as needed
    });
  };

  handlePositionChange = ({ coords }) => {
    if (this.state.isLogging) {
      const { latitude, longitude } = coords;
      if (this.state.lastPosition) {
        const distance = this.calculateDistance(
          this.state.lastPosition.latitude,
          this.state.lastPosition.longitude,
          latitude,
          longitude
        );
        this.setState(prevState => ({
          totalDistance: prevState.totalDistance + distance,
          lastPosition: { latitude, longitude },
        }));
      } else {
        this.setState({
          lastPosition: { latitude, longitude },
        });
      }
    }
  };

  calculateDistance(lat1, lon1, lat2, lon2) {
    // Haversine formula to calculate distance between two coordinates in meters
    const R = 6371e3; // Earth radius in meters
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // Distance in meters
  }

  render() {
    return (
      <div>
        <button onClick={this.startLogging}>Start Distance Logging</button>
        <button onClick={this.stopLogging}>Stop Distance Logging</button>
        <div>Total Distance: {this.state.totalDistance.toFixed(2)} meters</div>
      </div>
    );
  }
}

export default DistanceLogger;