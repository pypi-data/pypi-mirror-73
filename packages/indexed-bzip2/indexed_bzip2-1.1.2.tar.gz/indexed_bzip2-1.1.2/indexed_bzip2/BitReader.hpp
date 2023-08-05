#pragma once

#include <stdint.h>
#include <stdio.h>

#include <cassert>
#include <cstddef>
#include <stdexcept>
#include <sstream>
#include <string>
#include <vector>

#include <unistd.h>

#include "FileReader.hpp"


class BitReader :
    public FileReader
{
public:
    static constexpr size_t IOBUF_SIZE = 4096;
    static constexpr int NO_FILE = -1;

public:
    explicit
    BitReader( std::string filePath ) :
        m_file( fopen( filePath.c_str(), "rb" ) )
    {
        init();
    }

    explicit
    BitReader( int fileDescriptor ) :
        m_file( fdopen( dup( fileDescriptor ), "rb" ) )
    {
        init();
    }

    BitReader( const uint8_t* buffer,
               size_t         size ) :
        m_fileSizeBytes( size ),
        m_inbuf( buffer, buffer + size )
    {}

    BitReader( BitReader&& ) = default;

    /**
     * Copy constructor opens a new independent file descriptor and pointer.
     */
    BitReader( const BitReader& other ) :
        m_file( other.m_file == nullptr ? nullptr : fdopen( dup( ::fileno( other.m_file ) ), "rb" ) )
    {}

    /**
     * Reassignment would have to close the old file and open a new.
     * Reusing the same file reader for a different file seems error prone.
     * If you really want that, just create a new object.
     */
    BitReader& operator=( const BitReader& ) = delete;

    BitReader& operator=( BitReader&& ) = delete;

    ~BitReader()
    {
        if ( m_file != nullptr ) {
            fclose( m_file );
        }
    }

    bool
    eof() const override
    {
        return tell() >= size();
    }

    void
    close() override
    {
        fclose( fp() );
        m_file = nullptr;
        m_inbuf.clear();
    }

    bool
    closed() const override
    {
        return ( m_file == nullptr ) && m_inbuf.empty();
    }

    uint32_t
    read( uint8_t );

    /**
     * @return current position / number of bits already read.
     */
    size_t
    tell() const override
    {
        return ( ftell( fp() ) - m_inbuf.size() + m_inbufPos ) * 8ULL - m_inbufBitCount;
    }

    FILE*
    fp() const
    {
        return m_file;
    }

    int
    fileno() const override
    {
        if ( m_file == nullptr ) {
            throw std::invalid_argument( "The file is not open!" );
        }
        return ::fileno( m_file );
    }

    size_t
    seek( long long int offsetBits,
          int           origin = SEEK_SET ) override;

    size_t
    size() const override
    {
        return m_fileSizeBytes * 8;
    }

private:
    void
    init()
    {
        fseek( fp(), 0, SEEK_END );
        m_fileSizeBytes = ftell( fp() );
        fseek( fp(), 0, SEEK_SET ); /* good to have even when not getting the size! */
    }

private:
    FILE* m_file = nullptr;
    size_t m_fileSizeBytes = 0;
    std::vector<uint8_t> m_inbuf;
    uint32_t m_inbufPos = 0; /** stores current position of first valid byte in buffer */

public:
    /**
     * Bit buffer stores the last read bits from m_inbuf.
     * The bits are to be read from left to right. This means that not the least significant n bits
     * are to be returned on read but the most significant.
     * E.g. return 3 bits of 1011 1001 should return 101 not 001
     */
    uint32_t m_inbufBits = 0;
    uint8_t m_inbufBitCount = 0; // size of bitbuffer in bits
};


inline uint32_t
BitReader::read( const uint8_t bits_wanted )
{
    uint32_t bits = 0;
    assert( bits_wanted <= sizeof( bits ) * 8 );

    // If we need to get more data from the byte buffer, do so.  (Loop getting
    // one byte at a time to enforce endianness and avoid unaligned access.)
    auto bitsNeeded = bits_wanted;
    while ( m_inbufBitCount < bitsNeeded ) {
        // If we need to read more data from file into byte buffer, do so
        if ( m_inbufPos == m_inbuf.size() ) {
            m_inbuf.resize( IOBUF_SIZE );
            const auto nBytesRead = fread( m_inbuf.data(), 1, m_inbuf.size(), m_file );
            if ( nBytesRead <= 0 ) {
                // this will also happen for invalid file descriptor -1
                std::stringstream msg;
                msg
                << "[BitReader] Not enough data to read!\n"
                << "  File pointer: " << (void*)m_file << "\n"
                << "  File position: " << ftell( m_file ) << "\n"
                << "  Input buffer size: " << m_inbuf.size() << "\n"
                << "\n";
                throw std::domain_error( msg.str() );
            }
            m_inbuf.resize( nBytesRead );
            m_inbufPos = 0;
        }

        // Avoid 32-bit overflow (dump bit buffer to top of output)
        if ( m_inbufBitCount >= 24 ) {
            bits = m_inbufBits & ( ( 1 << m_inbufBitCount ) - 1 );
            bitsNeeded -= m_inbufBitCount;
            bits <<= bitsNeeded;
            m_inbufBitCount = 0;
        }

        // Grab next 8 bits of input from buffer.
        m_inbufBits = ( m_inbufBits << 8 ) | m_inbuf[m_inbufPos++];
        m_inbufBitCount += 8;
    }

    // Calculate result
    m_inbufBitCount -= bitsNeeded;
    bits |= ( m_inbufBits >> m_inbufBitCount ) & ( ( 1 << bitsNeeded ) - 1 );
    assert( bits == ( bits & ( ~0L >> ( 32 - bits_wanted ) ) ) );
    return bits;
}


inline size_t
BitReader::seek( long long int offsetBits,
                 int           origin )
{
    switch ( origin )
    {
    case SEEK_CUR:
        offsetBits = tell() + offsetBits;
        break;
    case SEEK_SET:
        break;
    case SEEK_END:
        offsetBits = size() + offsetBits;
        break;
    }

    if ( offsetBits < 0 ) {
        throw std::invalid_argument( "Effective offset is before file start!" );
    }

    if ( static_cast<size_t>( offsetBits ) >= size() ) {
        throw std::invalid_argument( "Effective offset is after file end!" );
    }

    if ( static_cast<size_t>( offsetBits ) == tell() ) {
        return offsetBits;
    }

    const size_t bytesToSeek = offsetBits >> 3;
    const size_t subBitsToSeek = offsetBits & 7;

    m_inbuf.clear();
    m_inbufPos = 0;
    m_inbufBits = 0;
    m_inbufBitCount = 0;

    if ( m_file == nullptr ) {
        if ( bytesToSeek >= m_inbuf.size() ) {
            std::stringstream msg;
            msg << "[BitReader] Could not seek to specified byte " << bytesToSeek;
            std::invalid_argument( msg.str() );
        }

        m_inbufPos = bytesToSeek;
        if ( subBitsToSeek > 0 ) {
            m_inbufBitCount = 8 - subBitsToSeek;
            m_inbufBits = m_inbuf[m_inbufPos++];
        }
    } else {
        const auto returnCodeSeek = fseek( m_file, bytesToSeek, SEEK_SET );
        if ( subBitsToSeek > 0 ) {
            m_inbufBitCount = 8 - subBitsToSeek;
            m_inbufBits = fgetc( m_file );
        }

        if ( ( returnCodeSeek != 0 ) || feof( m_file ) || ferror( m_file ) ) {
            std::stringstream msg;
            msg << "[BitReader] Could not seek to specified byte " << bytesToSeek
            << " subbit " << subBitsToSeek << ", feof: " << feof( m_file ) << ", ferror: " << ferror( m_file )
            << ", returnCodeSeek: " << returnCodeSeek;
            throw std::invalid_argument( msg.str() );
        }
    }

    return offsetBits;
}
