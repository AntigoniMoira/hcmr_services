export default {
    home:{
        root:'',
        access_token: '/webapp/access_token/',
        platforms_between: '/webapp/platforms_between/',
        measurements_between: '/webapp/measurements_between/',
        create_netcdf: '/webapp/create_netcdf/',
        activate_user: '/webapp/activate/',
        delete_user: '/webapp/delete_user/',
        error: '/webapp/error',
        user_profile: '/webapp/user_profile/',
        change_password: '/webapp/change_password/',
        logout: '/webapp/logout/',
    },
    auth:{
        login: 'http://localhost:8000/o/authorize/',
        register: 'http://localhost:8000/auth/register/'
    }

}
