from typing import Tuple, List
from io import BytesIO
from enum import Enum
from tdata_decrypt.tdt import (
    TDRawBytes,
    TDInt32,
    TDUInt64,
    TDByteArray,
    TDString,
    TDBoolean
)

def read_key_data_accounts(data: BytesIO) -> Tuple[List[int], int]:
    count = TDInt32.read(data)

    indexes = [
        TDInt32.read(data)
        for _ in range(count)
    ]

    main_account = TDInt32.read(data)

    return indexes, main_account

class SettingsBlocks(Enum):
    dbiKey = 0x00
    dbiUser = 0x01
    dbiDcOptionOldOld = 0x02
    dbiChatSizeMaxOld = 0x03
    dbiMutePeerOld = 0x04
    dbiSendKeyOld = 0x05
    dbiAutoStart = 0x06
    dbiStartMinimized = 0x07
    dbiSoundFlashBounceNotifyOld = 0x08
    dbiWorkModeOld = 0x09
    dbiSeenTrayTooltip = 0x0a
    dbiDesktopNotifyOld = 0x0b
    dbiAutoUpdate = 0x0c
    dbiLastUpdateCheck = 0x0d
    dbiWindowPositionOld = 0x0e
    dbiConnectionTypeOldOld = 0x0f
    dbiDefaultAttach = 0x11
    dbiCatsAndDogsOld = 0x12
    dbiReplaceEmojiOld = 0x13
    dbiAskDownloadPathOld = 0x14
    dbiDownloadPathOldOld = 0x15
    dbiScaleOld = 0x16
    dbiEmojiTabOld = 0x17
    dbiRecentEmojiOldOldOld = 0x18
    dbiLoggedPhoneNumberOld = 0x19
    dbiMutedPeersOld = 0x1a
    dbiNotifyViewOld = 0x1c
    dbiSendToMenu = 0x1d
    dbiCompressPastedImageOld = 0x1e
    dbiLangOld = 0x1f
    dbiLangFileOld = 0x20
    dbiTileBackgroundOld = 0x21
    dbiAutoLockOld = 0x22
    dbiDialogLastPath = 0x23
    dbiRecentEmojiOldOld = 0x24
    dbiEmojiVariantsOldOld = 0x25
    dbiRecentStickers = 0x26
    dbiDcOptionOld = 0x27
    dbiTryIPv6Old = 0x28
    dbiSongVolumeOld = 0x29
    dbiWindowsNotificationsOld = 0x30
    dbiIncludeMutedOld = 0x31
    dbiMegagroupSizeMaxOld = 0x32
    dbiDownloadPathOld = 0x33
    dbiAutoDownloadOld = 0x34
    dbiSavedGifsLimitOld = 0x35
    dbiShowingSavedGifsOld = 0x36
    dbiAutoPlayOld = 0x37
    dbiAdaptiveForWideOld = 0x38
    dbiHiddenPinnedMessagesOld = 0x39
    dbiRecentEmojiOld = 0x3a
    dbiEmojiVariantsOld = 0x3b
    dbiDialogsModeOld = 0x40
    dbiModerateModeOld = 0x41
    dbiVideoVolumeOld = 0x42
    dbiStickersRecentLimitOld = 0x43
    dbiNativeNotificationsOld = 0x44
    dbiNotificationsCountOld = 0x45
    dbiNotificationsCornerOld = 0x46
    dbiThemeKeyOld = 0x47
    dbiDialogsWidthRatioOld = 0x48
    dbiUseExternalVideoPlayerOld = 0x49
    dbiDcOptionsOld = 0x4a
    dbiMtpAuthorization = 0x4b
    dbiLastSeenWarningSeenOld = 0x4c
    dbiSessionSettings = 0x4d
    dbiLangPackKey = 0x4e
    dbiConnectionTypeOld = 0x4f
    dbiStickersFavedLimitOld = 0x50
    dbiSuggestStickersByEmojiOld = 0x51
    dbiSuggestEmojiOld = 0x52
    dbiTxtDomainStringOldOld = 0x53
    dbiThemeKey = 0x54
    dbiTileBackground = 0x55
    dbiCacheSettingsOld = 0x56
    dbiPowerSaving = 0x57
    dbiScalePercent = 0x58
    dbiPlaybackSpeedOld = 0x59
    dbiLanguagesKey = 0x5a
    dbiCallSettingsOld = 0x5b
    dbiCacheSettings = 0x5c
    dbiTxtDomainStringOld = 0x5d
    dbiApplicationSettings = 0x5e
    dbiDialogsFiltersOld = 0x5f
    dbiFallbackProductionConfig = 0x60
    dbiBackgroundKey = 0x61
    dbiEncryptedWithSalt = 333
    dbiEncrypted = 444
    dbiVersion = 666

class TDOSongVolumeOld(TDInt32):
    @classmethod
    def read(cls, data: BytesIO) -> float:
        return cls._read_value(data) / 1e6

class TDOdbiThemeKey(TDRawBytes):
    size = TDUInt64.size + TDUInt64.size + TDBoolean.size

    @classmethod
    def read(cls, data: BytesIO):
        return {
            'day': TDUInt64.read(data),
            'night': TDUInt64.read(data),
            'night_mode': TDBoolean.read(data)
        }

class TDOdbiBackgroundKey(TDRawBytes):
    size = TDUInt64.size + TDUInt64.size

    @classmethod
    def read(cls, data: BytesIO):
        return {
            'day': TDUInt64.read(data),
            'night': TDUInt64.read(data)
        }

class TDOdbiTileBackground(TDRawBytes):
    size = TDInt32.size + TDInt32.size

    @classmethod
    def read(cls, data: BytesIO):
        return {
            'day': TDInt32.read(data),
            'night': TDInt32.read(data)
        }


class Settings:
    LUT = {
        SettingsBlocks.dbiAutoStart: TDBoolean,
        SettingsBlocks.dbiStartMinimized: TDBoolean,
        SettingsBlocks.dbiSongVolumeOld: TDOSongVolumeOld,
        SettingsBlocks.dbiSendToMenu: TDBoolean,
        SettingsBlocks.dbiSeenTrayTooltip: TDBoolean,
        SettingsBlocks.dbiAutoUpdate: TDBoolean,
        SettingsBlocks.dbiLastUpdateCheck: TDInt32,
        SettingsBlocks.dbiScalePercent: TDInt32,
        SettingsBlocks.dbiFallbackProductionConfig: TDByteArray,
        SettingsBlocks.dbiApplicationSettings: TDByteArray,
        SettingsBlocks.dbiDialogLastPath: TDString,
        SettingsBlocks.dbiPowerSaving: TDInt32,
        SettingsBlocks.dbiThemeKey: TDOdbiThemeKey,
        SettingsBlocks.dbiBackgroundKey: TDOdbiBackgroundKey,
        SettingsBlocks.dbiTileBackground: TDOdbiTileBackground,
        SettingsBlocks.dbiLangPackKey: TDUInt64,
        SettingsBlocks.dbiMtpAuthorization: TDByteArray,
        SettingsBlocks.dbiLanguagesKey:  TDUInt64
    }

    @classmethod
    def read_value(cls, verison, data: BytesIO, block_id: SettingsBlocks):
        call = cls.LUT.get(block_id)
        if not call:
            raise Exception(f'Unknown settings block ID: {block_id}')

        return call.read(data)


def read_settings_blocks(version, data: BytesIO):
    blocks = {}

    try:
        while True:
            id = SettingsBlocks(TDInt32.read(data))
            blocks[id] = Settings.read_value(version, data, id)

    except StopIteration:
        pass

    return blocks

class SettingsReader:
    pass
