// package: 
// file: playwright.proto

/* tslint:disable */
/* eslint-disable */

import * as jspb from "google-protobuf";

export class Request extends jspb.Message { 

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Request.AsObject;
    static toObject(includeInstance: boolean, msg: Request): Request.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Request, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Request;
    static deserializeBinaryFromReader(message: Request, reader: jspb.BinaryReader): Request;
}

export namespace Request {
    export type AsObject = {
    }


    export class Empty extends jspb.Message { 

        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Empty.AsObject;
        static toObject(includeInstance: boolean, msg: Empty): Empty.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Empty, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Empty;
        static deserializeBinaryFromReader(message: Empty, reader: jspb.BinaryReader): Empty;
    }

    export namespace Empty {
        export type AsObject = {
        }
    }

    export class screenshot extends jspb.Message { 
        getPath(): string;
        setPath(value: string): screenshot;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): screenshot.AsObject;
        static toObject(includeInstance: boolean, msg: screenshot): screenshot.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: screenshot, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): screenshot;
        static deserializeBinaryFromReader(message: screenshot, reader: jspb.BinaryReader): screenshot;
    }

    export namespace screenshot {
        export type AsObject = {
            path: string,
        }
    }

    export class openBrowser extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): openBrowser;

        getBrowser(): string;
        setBrowser(value: string): openBrowser;

        getHeadless(): boolean;
        setHeadless(value: boolean): openBrowser;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): openBrowser.AsObject;
        static toObject(includeInstance: boolean, msg: openBrowser): openBrowser.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: openBrowser, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): openBrowser;
        static deserializeBinaryFromReader(message: openBrowser, reader: jspb.BinaryReader): openBrowser;
    }

    export namespace openBrowser {
        export type AsObject = {
            url: string,
            browser: string,
            headless: boolean,
        }
    }

    export class goTo extends jspb.Message { 
        getUrl(): string;
        setUrl(value: string): goTo;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): goTo.AsObject;
        static toObject(includeInstance: boolean, msg: goTo): goTo.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: goTo, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): goTo;
        static deserializeBinaryFromReader(message: goTo, reader: jspb.BinaryReader): goTo;
    }

    export namespace goTo {
        export type AsObject = {
            url: string,
        }
    }

    export class inputText extends jspb.Message { 
        getInput(): string;
        setInput(value: string): inputText;

        getSelector(): string;
        setSelector(value: string): inputText;

        getType(): boolean;
        setType(value: boolean): inputText;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): inputText.AsObject;
        static toObject(includeInstance: boolean, msg: inputText): inputText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: inputText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): inputText;
        static deserializeBinaryFromReader(message: inputText, reader: jspb.BinaryReader): inputText;
    }

    export namespace inputText {
        export type AsObject = {
            input: string,
            selector: string,
            type: boolean,
        }
    }

    export class getDomProperty extends jspb.Message { 
        getProperty(): string;
        setProperty(value: string): getDomProperty;

        getSelector(): string;
        setSelector(value: string): getDomProperty;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): getDomProperty.AsObject;
        static toObject(includeInstance: boolean, msg: getDomProperty): getDomProperty.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: getDomProperty, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): getDomProperty;
        static deserializeBinaryFromReader(message: getDomProperty, reader: jspb.BinaryReader): getDomProperty;
    }

    export namespace getDomProperty {
        export type AsObject = {
            property: string,
            selector: string,
        }
    }

    export class typeText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): typeText;

        getText(): string;
        setText(value: string): typeText;

        getDelay(): number;
        setDelay(value: number): typeText;

        getClear(): boolean;
        setClear(value: boolean): typeText;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): typeText.AsObject;
        static toObject(includeInstance: boolean, msg: typeText): typeText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: typeText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): typeText;
        static deserializeBinaryFromReader(message: typeText, reader: jspb.BinaryReader): typeText;
    }

    export namespace typeText {
        export type AsObject = {
            selector: string,
            text: string,
            delay: number,
            clear: boolean,
        }
    }

    export class fillText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): fillText;

        getText(): string;
        setText(value: string): fillText;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): fillText.AsObject;
        static toObject(includeInstance: boolean, msg: fillText): fillText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: fillText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): fillText;
        static deserializeBinaryFromReader(message: fillText, reader: jspb.BinaryReader): fillText;
    }

    export namespace fillText {
        export type AsObject = {
            selector: string,
            text: string,
        }
    }

    export class clearText extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): clearText;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): clearText.AsObject;
        static toObject(includeInstance: boolean, msg: clearText): clearText.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: clearText, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): clearText;
        static deserializeBinaryFromReader(message: clearText, reader: jspb.BinaryReader): clearText;
    }

    export namespace clearText {
        export type AsObject = {
            selector: string,
        }
    }

    export class press extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): press;

        clearKeyList(): void;
        getKeyList(): Array<string>;
        setKeyList(value: Array<string>): press;
        addKey(value: string, index?: number): string;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): press.AsObject;
        static toObject(includeInstance: boolean, msg: press): press.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: press, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): press;
        static deserializeBinaryFromReader(message: press, reader: jspb.BinaryReader): press;
    }

    export namespace press {
        export type AsObject = {
            selector: string,
            keyList: Array<string>,
        }
    }

    export class selector extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): selector;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): selector.AsObject;
        static toObject(includeInstance: boolean, msg: selector): selector.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: selector, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): selector;
        static deserializeBinaryFromReader(message: selector, reader: jspb.BinaryReader): selector;
    }

    export namespace selector {
        export type AsObject = {
            selector: string,
        }
    }

    export class timeout extends jspb.Message { 
        getTimeout(): number;
        setTimeout(value: number): timeout;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): timeout.AsObject;
        static toObject(includeInstance: boolean, msg: timeout): timeout.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: timeout, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): timeout;
        static deserializeBinaryFromReader(message: timeout, reader: jspb.BinaryReader): timeout;
    }

    export namespace timeout {
        export type AsObject = {
            timeout: number,
        }
    }

    export class addStyleTag extends jspb.Message { 
        getContent(): string;
        setContent(value: string): addStyleTag;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): addStyleTag.AsObject;
        static toObject(includeInstance: boolean, msg: addStyleTag): addStyleTag.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: addStyleTag, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): addStyleTag;
        static deserializeBinaryFromReader(message: addStyleTag, reader: jspb.BinaryReader): addStyleTag;
    }

    export namespace addStyleTag {
        export type AsObject = {
            content: string,
        }
    }

    export class selectorOptions extends jspb.Message { 
        getSelector(): string;
        setSelector(value: string): selectorOptions;

        getOptions(): string;
        setOptions(value: string): selectorOptions;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): selectorOptions.AsObject;
        static toObject(includeInstance: boolean, msg: selectorOptions): selectorOptions.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: selectorOptions, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): selectorOptions;
        static deserializeBinaryFromReader(message: selectorOptions, reader: jspb.BinaryReader): selectorOptions;
    }

    export namespace selectorOptions {
        export type AsObject = {
            selector: string,
            options: string,
        }
    }

}

export class Response extends jspb.Message { 

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Response.AsObject;
    static toObject(includeInstance: boolean, msg: Response): Response.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Response, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Response;
    static deserializeBinaryFromReader(message: Response, reader: jspb.BinaryReader): Response;
}

export namespace Response {
    export type AsObject = {
    }


    export class Empty extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Empty;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Empty.AsObject;
        static toObject(includeInstance: boolean, msg: Empty): Empty.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Empty, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Empty;
        static deserializeBinaryFromReader(message: Empty, reader: jspb.BinaryReader): Empty;
    }

    export namespace Empty {
        export type AsObject = {
            log: string,
        }
    }

    export class String extends jspb.Message { 
        getLog(): string;
        setLog(value: string): String;

        getBody(): string;
        setBody(value: string): String;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): String.AsObject;
        static toObject(includeInstance: boolean, msg: String): String.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: String, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): String;
        static deserializeBinaryFromReader(message: String, reader: jspb.BinaryReader): String;
    }

    export namespace String {
        export type AsObject = {
            log: string,
            body: string,
        }
    }

    export class Bool extends jspb.Message { 
        getLog(): string;
        setLog(value: string): Bool;

        getBody(): boolean;
        setBody(value: boolean): Bool;


        serializeBinary(): Uint8Array;
        toObject(includeInstance?: boolean): Bool.AsObject;
        static toObject(includeInstance: boolean, msg: Bool): Bool.AsObject;
        static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
        static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
        static serializeBinaryToWriter(message: Bool, writer: jspb.BinaryWriter): void;
        static deserializeBinary(bytes: Uint8Array): Bool;
        static deserializeBinaryFromReader(message: Bool, reader: jspb.BinaryReader): Bool;
    }

    export namespace Bool {
        export type AsObject = {
            log: string,
            body: boolean,
        }
    }

}
