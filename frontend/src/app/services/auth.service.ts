import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';

import { environment } from '../../environments/environment';
import {catchError, shareReplay} from "rxjs/operators";
import {from, Observable, throwError} from "rxjs";
import createAuth0Client from '@auth0/auth0-spa-js';
import Auth0Client from '@auth0/auth0-spa-js/dist/typings/Auth0Client';

const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = environment.auth0.url;
  audience = environment.auth0.audience;
  clientId = environment.auth0.clientId;
  callbackURL = environment.auth0.callbackURL;

  token: string;
  payload: any;

  // Create an observable of Auth0 instance of client
  auth0Client$ = (from(
      createAuth0Client({
        domain: this.url + '.auth0.com',
        client_id: this.clientId,
        redirect_uri: `${window.location.origin}`
      })
  ) as Observable<Auth0Client>).pipe(
      shareReplay(1), // Every subscription receives the same shared value
      catchError(err => throwError(err))
  );

  constructor() { }

  build_login_link(callbackPath = '') {
    let link = 'https://';
    link += this.url + '.auth0.com';
    link += '/authorize?';
    link += 'audience=' + this.audience + '&';
    link += 'response_type=token&';
    link += 'client_id=' + this.clientId + '&';
    link += 'redirect_uri=' + this.callbackURL + callbackPath;
    return link;
  }

  // invoked in app.component on load
  check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if ( fragment[0] === 'access_token' ) {
      // add the access token to the jwt
      this.token = fragment[1];
      // save jwts to localstore
      this.set_jwt();
    }
  }

  set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  load_jwts() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  activeJWT() {
    return this.token;
  }

  decodeJWT(token: string) {
    const jwtservice = new JwtHelperService();
    this.payload = jwtservice.decodeToken(token);
    return this.payload;
  }

  logout() {
    this.token = '';
    this.payload = null;
    this.set_jwt();
    // Ensure Auth0 client instance exists
    this.auth0Client$.subscribe((client: Auth0Client) => {
      // Call method to log out
      client.logout({
        client_id: this.clientId,
        returnTo: `${window.location.origin}`
      });
    });
  }

  can(permission: string) {
    return this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0;
  }
}
