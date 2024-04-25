const path = require('path');
const webpack = require('webpack');
const appName = 'app';

//CommonJS syntax when exporting the module
module.exports = {
    entry: {
        appName: path.join(__dirname, 'src', 'index.js')
    },
    output: {
        filename: appName+'.bundle.js',
        path: path.resolve(__dirname, 'public')
    },
    module: {
        rules: [{
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader'
            }
        },
                {
            test: /\.css$/i,
            use: ['style-loader', 'css-loader']
        },
        {
            test: /\.(png|jpe?g|gif)$/i,
            loader: 'file-loader',
        }]
    },
    devServer: {
        static: {
            directory: path.join(__dirname, 'public'),
        },
	port: 8090,
        allowedHosts: 'all',
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ],
    watchOptions: {
        ignored: '**/node_modules',
    },
};
